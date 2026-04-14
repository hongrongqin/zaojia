from common.response.code_base import BaseStatus
from common.response import StatusEnum


def create_custom_exception(status):
    class CustomException(BaseCustomException):
        def __init__(self, msg=None):
            super().__init__(msg, status)

    return CustomException


class BaseCustomException(Exception):
    """
    自定义异常 基类
    """

    def __init__(self, msg: str, status: StatusEnum, data=None):
        self.status = status
        self.msg = msg
        self.data = data


ClientError = create_custom_exception(BaseStatus.CLIENT_ERROR)
MissParams = create_custom_exception(BaseStatus.MISS_PARAMS)
UnknownError = create_custom_exception(BaseStatus.UNKNOWN_ERROR)
Unauthorized = create_custom_exception(BaseStatus.UNAUTHORIZED)
Forbidden = create_custom_exception(BaseStatus.FORBIDDEN)
TooManyRequest = create_custom_exception(BaseStatus.TOO_MANY_REQUEST)
ValidatorError = create_custom_exception(BaseStatus.VALIDATOR_ERROR)
