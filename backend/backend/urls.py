"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from rest_framework.schemas import get_schema_view

schema_view = get_schema_view(
    title='Your API',  # API 文档的标题
    version='1.0',      # API 版本
    description='API for your application',  # API 文档的描述
    public=True,        # 如果设置为 True，将允许任何人查看 API 文档
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('oauth/', include('system.urls')),
    path('schema/', schema_view, name='schema'),  # 添加这一行
]
