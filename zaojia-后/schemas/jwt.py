from fastapi.security import OAuth2PasswordBearer
from pydantic import Field

from schemas.base import BaseSchema

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")


class UserInfo(BaseSchema):
    uid: str = Field(..., min_length=3, max_length=50, description="用户唯一标识，目前对应数据库id")
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    role_type: str = Field(default="用户", max_length=50, description="身份")
    phone: str | None = Field(None, max_length=64, description="手机号")
