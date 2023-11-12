import time
from rest_framework.permissions import BasePermission

from config import config
from system.models import Permission


class RouterNameMeta(type):
    """自定义路由名称处理"""
    def __new__(cls, name, bases, attr):
        if 'router_name' in attr:
            assert attr['router_name'] not in config.ROUTER_NAMES, f'路由名称{attr["router_name"]}已经存在了'
            config.ROUTER_NAMES.append({
                'router_name': attr['router_name'],
                'router_desc': attr.get('router_desc', '')
            })
        return super().__new__(cls, name, bases, attr)


class VisitorPermission(BasePermission):
    """访问权限控制"""

    def has_permission(self, request, view):
        if hasattr(view, 'router_name'):
            permission = request.user.get_user_permissions()
            has_perm = Permission.objects.filter(
                id__in=permission, name=view.router_name, method=request.method
            ).exists()
            if not has_perm:
                return False
        self.flush_permission_check(request, view)
        return True

    @staticmethod
    def flush_permission_check(request, view):
        if request.method not in ["POST", "PUT", "DELETE"]:
            return
        from system.views.admin import PermissionView, RoleView, MenuView, UserView
        if not isinstance(view, (PermissionView, RoleView, MenuView, UserView)):
            return
        config.PERM_UPDATE_TS = int(time.time())
