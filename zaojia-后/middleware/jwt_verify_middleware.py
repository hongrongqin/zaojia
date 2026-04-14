from fastapi import Depends, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from common.response.schema import responseBase
from common.response.code_user import UserStatus

from schemas.jwt import UserInfo
from services.jwt import JwtService


class JwtVerifyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # 暂时取消 token 认证限制所有路由
        response = await call_next(request)
        return response
