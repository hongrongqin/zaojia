from datetime import datetime
from pydantic import Field

from schemas.base import BaseSchema


class HttpLogin(BaseSchema):
    username: str = Field(max_length=50, description="用户名")
    password: str = Field(min_length=6, max_length=100, description="用户密码")
    code: str = Field(..., max_length=10, description="验证码")
    uuid: str = Field(..., max_length=100, description="验证码唯一标识")


# 用户注册
class HttpCreateUser(BaseSchema):
    username: str = Field(..., max_length=50, description="用户名")
    password: str = Field(..., min_length=6, max_length=100, description="密码")
    phone: str = Field(..., max_length=20, description="手机号")

# 创建用户入库
class DataBaseCreateUser(BaseSchema):
    uid: str = Field(..., description="用户id")
    username: str = Field(..., max_length=50, description="用户名")
    password: str = Field(..., max_length=100, description="密码")
    phone: str = Field(..., max_length=20, description="手机号")

