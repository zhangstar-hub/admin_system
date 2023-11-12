import time

from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from config import config


class ExceptionHandlerMiddleware(MiddlewareMixin):

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            return JsonResponse({'detail': ['页面或接口不存在']}, status=404)
        return response


class PermissionMiddleware(MiddlewareMixin):

    def __call__(self, request):
        response = self.get_response(request)
        try:
            before_perm_ts = int(request.headers['Perm-Update-Ts'])
        except (TypeError, KeyError, ValueError, AttributeError):
            before_perm_ts = None
        if before_perm_ts and before_perm_ts < config.PERM_UPDATE_TS:
            print(config.PERM_UPDATE_TS, before_perm_ts)
            response['Perm-Update-Ts'] = int(time.time())
        return response
