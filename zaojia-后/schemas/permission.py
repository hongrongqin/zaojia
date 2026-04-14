from schemas.base import BaseSchema
from pydantic import Field


class DataBaseCreatePermission(BaseSchema):
    pid: str = Field(..., min_length=3, max_length=50, description="权限唯一标识")
    permission: str = Field(..., max_length=50, description="角色名称")
