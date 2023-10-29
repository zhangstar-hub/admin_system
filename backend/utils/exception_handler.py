from rest_framework.exceptions import ValidationError, AuthenticationFailed, APIException
from rest_framework.views import exception_handler
from rest_framework.response import Response

from utils.status_code import ERR_MESSAGE


def custom_exception_handler(exc, context):

    def get_details(detail):
        if isinstance(detail, list):
            for i in detail:
                yield from get_details(i)
        elif isinstance(detail, dict):
            for i in detail.values():
                yield from get_details(i)
        else:
            yield detail

    if isinstance(exc, APIException):
        print(exc, exc.status_code, exc.detail)
        if exc.status_code in ERR_MESSAGE:
            return Response({"detail": ERR_MESSAGE[exc.status_code]}, status=exc.status_code)
        return Response({"detail": get_details(exc.detail)}, status=exc.status_code)
    response = exception_handler(exc, context)  # 使用 DRF 默认的异常处理器
    return response
