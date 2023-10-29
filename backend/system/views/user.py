from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from system.models import Permission, User, Menu, Role
from system.permission import RouterNameMeta, ROUTER_NAMES
from system.serializers import PermissionSerializer, UserSerializer, MenuSerializer, RoleSerializer


class LoginView(ObtainAuthToken):
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_data': UserSerializer(user).data})


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


class UserPersonal(GenericViewSet, metaclass=RouterNameMeta):
    router_name = 'user_personal'
    router_desc = "用户个人权限信息"
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True)
    def combo_info(self, request, pk=None):
        user = User.objects.get(pk=pk)
        user_data = self.serializer_class(user).data
        user_data['permissions'] = user.get_user_permissions()
        menu_ids = user.get_user_menus()
        menu_pids = Menu.objects.filter(
            id__in=menu_ids
        ).values_list('pid', flat=True)
        menus = MenuSerializer(
            Menu.objects.filter(id__in=menu_pids), many=True
        ).data
        for i in menus:
            i['children'] = [i for i in i['children'] if i['id'] in menu_ids]
        user_data['menus'] = menus
        return Response(user_data)


class PermissionView(ModelViewSet, metaclass=RouterNameMeta):
    router_name = 'permission'
    router_desc = "权限信息路由"
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

    def create(self, request, *args, **kwargs):
        data = []
        for i in request.data.get('methods', []):
            data.append({'method': i, **request.data})
        print(data)
        serializer = self.get_serializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False)
    def combo_info(self, request, *args, **kwargs):
        data = {
            'permissions': self.serializer_class(self.get_queryset().all(), many=True).data,
            'menus': MenuSerializer(Menu.objects.filter(pid=None), many=True).data,
            'router_names': ROUTER_NAMES
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
    router_name = 'test'
    router_desc = "测试路由"

    def get(self, request):
        raise ValidationError(detail="test error")


class RouterNameView(APIView, metaclass=RouterNameMeta):
    router_name = 'router_name'
    router_desc = "路由名称"

    def get(self, request):
        return Response(ROUTER_NAMES)
