try:
    from jwt.exceptions import InvalidTokenError
except Exception:
    try:
        from jwt.exceptions import JWTException as InvalidTokenError
    except Exception:
        from jwt.exceptions import PyJWTError as InvalidTokenError
import jwt
from typing import Union
from fastapi import Depends, status
from schemas.jwt import oauth2_schema, UserInfo
from starlette.exceptions import HTTPException
from core.config import settings
from datetime import timedelta, datetime, timezone
from dao.user import UserDao

class JwtService(object):

    @classmethod
    async def get_current_user(cls, token: str = ""): # 暂时不需要强制用Depends(oauth2_schema)
        # 暂时取消 token 认证，返回一个假的 UserInfo 用于测试
        return UserInfo(uid="test_user_id", username="test_user", role_type="admin")

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            uid: str = payload.get("uid")
            if uid is None:
                raise credentials_exception
        except InvalidTokenError:
            raise credentials_exception

        # 通过前端传来的 token 解码出 uid ，再通过 uid 查询数据中的数据
        # 可自定义 cls._get_user() 函数
        user = await UserDao.get_by_id(user_id=uid)
        if user is None:
            raise credentials_exception
        
        user_dict = user.__dict__.copy()
        # 模型主键是 id 但 UserInfo 需要 uid
        if "id" in user_dict:
            user_dict["uid"] = user_dict.pop("id")
            
        return UserInfo(**user_dict)

    @classmethod
    def create_access_token(cls, uid: str, username: str):
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        token = cls._create_access_token(
            data={"uid": uid, "username": username}, expires_delta=access_token_expires
        )
        expire_time = (datetime.now() + access_token_expires).strftime("%Y-%m-%d %H:%M:%S")
        return {"access_token": token, "expire": expire_time}

    @classmethod
    def _create_access_token(cls, data: dict, expires_delta: Union[timedelta, None] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    @classmethod
    async def _get_db_user_dict(cls):
        user_list = await UserDao.list_user()
        return {user.id: user for user in user_list}

    @classmethod
    def _get_user(cls, db_user_dict, uid: str):
        if uid in db_user_dict.keys():
            user = db_user_dict[uid]
            user_dict = user.__dict__.copy()
            if "id" in user_dict:
                user_dict["uid"] = user_dict.pop("id")
            return UserInfo(**user_dict)
