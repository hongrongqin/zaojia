# 创建异常类
from common.exception.exception_base import create_custom_exception
from common.response.code_user import UserStatus

AccountFrozen = create_custom_exception(UserStatus.ACCOUNT_FROZEN)
AccountExist = create_custom_exception(UserStatus.ACCOUNT_EXIST)
AccountNotExist = create_custom_exception(UserStatus.ACCOUNT_NOT_EXIST)
PassWordError = create_custom_exception(UserStatus.PASSWORD_ERROR)
NotAuthenticated = create_custom_exception(UserStatus.NOT_AUTHENTICATED)
CaptchaError = create_custom_exception(UserStatus.CAPTCHA_ERROR)
