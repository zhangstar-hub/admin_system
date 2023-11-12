from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework.exceptions import ValidationError


class ExceptionHandlerMiddleware(MiddlewareMixin):

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            return JsonResponse({'detail': ['页面或接口不存在']}, status=404)
        return response
