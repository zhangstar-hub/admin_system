from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from celery_task.sms_task import timer_send_sms
from system.models import Permission, User, Menu, Role
from system.permission import RouterNameMeta
from system.serializers import PermissionSerializer, UserSerializer, MenuSerializer, RoleSerializer
from config import config


class LoginView(ObtainAuthToken):
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
        except ValidationError:
            raise ValidationError(detail="用户名或者密码错误")
        response['Perm-Update-Ts'] = config.PERM_UPDATE_TS
        return response


class UserView(ModelViewSet, metaclass=RouterNameMeta):
    router_name = 'user'
    router_desc = "账号信息路由"
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False)
    def combo_info(self, request, *args, **kwargs):
        data = {
            'users': self.serializer_class(self.get_queryset().all(), many=True).data,
            'roles': RoleSerializer(Role.objects.all(), many=True).data,
        }
        return Response(data)


class UserPersonalView(GenericViewSet, metaclass=RouterNameMeta):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False)
    def combo_info(self, request):
        permission_ids = request.user.get_user_permissions()
        data = {
            'user_data': self.serializer_class(request.user).data,
            'permissions': PermissionSerializer(Permission.objects.filter(id__in=permission_ids), many=True).data
        }
        menu_ids = request.user.get_user_menus()
        menu_pids = Menu.objects.filter(
            id__in=menu_ids
        ).values_list('pid', flat=True)
        menus = MenuSerializer(
            Menu.objects.filter(id__in=menu_pids), many=True
        ).data
        for i in menus:
            i['children'] = [i for i in i['children'] if i['id'] in menu_ids]
        data['menus'] = menus
        return Response(data)


class PermissionView(ModelViewSet, metaclass=RouterNameMeta):
    router_name = 'permission'
    router_desc = "权限信息路由"
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

    def create(self, request, *args, **kwargs):
        data = []
        for i in request.data.get('methods', []):
            data.append({'method': i, **request.data})
        serializer = self.get_serializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False)
    def combo_info(self, request, *args, **kwargs):
        data = {
            'permissions': self.serializer_class(self.get_queryset().all(), many=True).data,
            'menus': MenuSerializer(Menu.objects.filter(pid=None), many=True).data,
            'router_names': config.ROUTER_NAMES
        }
        return Response(data)


class MenuView(ModelViewSet, metaclass=RouterNameMeta):
    router_name = 'menu'
    router_desc = "菜单信息路由"
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(pid=None))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RoleView(ModelViewSet, metaclass=RouterNameMeta):
    router_name = 'role'
    router_desc = "角色信息路由"
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    @action(detail=False)
    def base_list(self, request, *args, **kwargs):
        simple_data = self.get_queryset().all().values('id', 'name')
        return Response(simple_data)


class TestView(APIView, metaclass=RouterNameMeta):

    def get(self, request):
        timer_send_sms.delay()
        return Response()


class RouterNameView(APIView, metaclass=RouterNameMeta):

    def get(self, request):
        return Response(config.ROUTER_NAMES)
