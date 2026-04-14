from pydantic import Field

from schemas.base import BaseSchema


class DataBaseCreateRole(BaseSchema):
    rid: str = Field(..., min_length=3, max_length=50, description="角色唯一标识")
    role: str = Field(..., max_length=50, description="角色名称")


class DataBaseCreateRolePermission(BaseSchema):
    rid: str = Field(..., min_length=3, max_length=50, description="角色唯一标识")
    pid: str = Field(..., min_length=3, max_length=50, description="权限唯一标识")


class DataBaseCreateUserRole(BaseSchema):
    uid: str = Field(..., min_length=3, max_length=50, description="用户唯一标识")
    rid: str = Field(..., min_length=3, max_length=50, description="角色唯一标识")