from django.urls import include, path
from rest_framework import routers
from .views import user

router = routers.DefaultRouter()
router.register(r'user', user.UserView, basename='user')
router.register(r'menu', user.MenuView, basename='menu')
router.register(r'role', user.RoleView, basename='role')
router.register(r'permission', user.PermissionView, basename='permission')
router.register(r'user_personal', user.UserPersonal, basename='user_personal')

urlpatterns = [
    path('login', user.LoginView.as_view(), name='login'),
    path('test', user.TestView.as_view(), name='test'),
    path('router_name/', user.RouterNameView.as_view(), name='router_name'),
    path('', include(router.urls)),
]