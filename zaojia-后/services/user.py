import hashlib
from datetime import datetime
from uuid import uuid4
from common.exception.exception_user import *
from dao.user import UserDao
from schemas.jwt import UserInfo
from schemas.user import DataBaseCreateUser, HttpCreateUser, HttpLogin
from services.jwt import JwtService
from utils.captcha import verify_captcha, generate_captcha


class UserService(object):
    @classmethod
    def generate_password_md5(cls, password):
        md5 = hashlib.md5()
        md5.update(password.encode("utf8"))
        return md5.hexdigest()

    @classmethod
    async def login(cls, obj: HttpLogin):
        if not verify_captcha(obj.uuid, obj.code):
            raise CaptchaError()
            
        user = await UserDao.get_by_username(obj.username)
        if user is None:
            raise AccountNotExist(obj.username)
        if cls.generate_password_md5(obj.password) != user.password:
            raise PassWordError()
        
        token_data = JwtService.create_access_token(user.uid, obj.username)
        return {
            **token_data,
            "uid": user.uid,
            "username": user.username,
            "role_type": user.role_type
        }

    @classmethod
    async def create_user(cls, obj: HttpCreateUser):
        user = await UserDao.get_by_username(obj.username)
        if user:
            raise AccountExist("用户名已存在")
        obj.password = cls.generate_password_md5(obj.password)

        # 创建用户
        await UserDao.create_user(DataBaseCreateUser(
            **obj.model_dump(),
            uid=str(uuid4()),
        ))

    @classmethod
    async def list_user(cls):
        return await UserDao.list_user()

    @classmethod
    async def update_user(cls, obj: HttpCreateUser, user: UserInfo):
        user = await UserDao.get_by_id(user.uid)
        for key in obj.__dict__.keys():
            if key == "password":
                setattr(user, key, cls.generate_password_md5(getattr(obj, key)))
            else:
                setattr(user, key, getattr(obj, key))
        await UserDao.update(user)
