# 用户认证接口
from fastapi import APIRouter, Depends, Security
from common.response.schema import responseBase
from schemas.jwt import UserInfo
from schemas.user import *
from services.jwt import JwtService
from services.user import UserService
from utils.captcha import generate_captcha

router = APIRouter()

@router.get("/captchaImage", summary="获取图片验证码")
async def get_captcha_image():
    """返回base64编码的图片和uuid"""
    data = generate_captcha()
    return await responseBase.success(data=data)

@router.get("/info",
            summary="获取当前用户信息",
            # dependencies=[Security(check_user, scopes=["check_self_info"])]
            )
async def user_info(user: UserInfo = Depends(JwtService.get_current_user)):
    return await responseBase.success(data=user)


@router.post("/login", summary="账号密码登录")
async def login(obj: HttpLogin):
    resp = await UserService.login(obj)
    return await responseBase.success(data=resp)


@router.post("/register", summary="新建用户",
             # dependencies=[Security(check_user, scopes=["create_user"])]
             )
async def create_user(obj: HttpCreateUser):
    await UserService.create_user(obj)
    return await responseBase.success()


@router.get("/list", summary="获取用户列表",
            # dependencies=[Security(check_user, scopes=["check_user"])]
            )
async def list_user():
    users = await UserService.list_user()
    return await responseBase.success(data=users)


@router.post("/update", summary="更新用户信息",
             # dependencies=[Security(check_user, scopes=["update_user"])]
             )
async def update_user(obj: HttpCreateUser, user: UserInfo = Depends(JwtService.get_current_user)):
    await UserService.update_user(obj, user)
    return await responseBase.success()
