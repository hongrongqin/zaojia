import asyncio
import json
import sys
from contextlib import asynccontextmanager

import fastapi_cdn_host
from fastapi import FastAPI
from common.exception.handler import register_exception
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware

from database.db import init_db
from middleware.access_middleware import AccessMiddleware
from middleware.jwt_verify_middleware import JwtVerifyMiddleware
from utils.health_check import ensure_unique_route_names
from controller.routers import v1
from core.config import settings


# 启动初始化
@asynccontextmanager
async def register_init(app: FastAPI):
    await init_db()  # 初始化数据库(初始化数据表)
    # await test_mysql()
    # await test_redis()
    # await test_mongo()
    yield

    # 关闭 redis
    # await redis_client.close()


def register_app():
    app = FastAPI(lifespan=register_init)
    # CDN
    fastapi_cdn_host.patch_docs(app)
    # 中间件
    register_middleware(app)
    # 路由
    register_router(app)
    # 全局异常处理
    register_exception(app)

    return app


def register_middleware(app) -> None:
    """
    中间件
    :param app:
    :return:
    """
    middleware_gzip = settings.MIDDLEWARE_GZIP
    middleware_access = settings.MIDDLEWARE_ACCESS
    middleware_cors = settings.MIDDLEWARE_CORS

    # gzip
    if middleware_gzip:
        app.add_middleware(GZipMiddleware)
    # 接口访问日志
    if middleware_access:
        app.add_middleware(AccessMiddleware)
        app.add_middleware(JwtVerifyMiddleware)
    # 跨域
    if middleware_cors:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )


def register_router(app: FastAPI):
    """
    路由注册
    :param app:
    :return:
    """
    app.include_router(v1)
    # 额外检查路由是否唯一
    ensure_unique_route_names(app)
