from django.urls import include, path
from rest_framework import routers
from .views import admin, monitor

router = routers.DefaultRouter()
router.register(r'user', admin.UserView, basename='user')
router.register(r'menu', admin.MenuView, basename='menu')
router.register(r'role', admin.RoleView, basename='role')
router.register(r'permission', admin.PermissionView, basename='permission')
router.register(r'user_personal', admin.UserPersonalView, basename='user_personal')
router.register(r'sms_monitor', monitor.SmsMonitorView, basename='sms_monitor')
router.register(r'sms', monitor.SmsView, basename='sms')

urlpatterns = [
    path('login', admin.LoginView.as_view(), name='login'),
    path('test', admin.TestView.as_view(), name='test'),
    path('router_name/', admin.RouterNameView.as_view(), name='router_name'),
    path('', include(router.urls)),
]