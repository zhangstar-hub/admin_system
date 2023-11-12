# celery.py
from __future__ import absolute_import, unicode_literals
import os
from datetime import timedelta

from celery import Celery

# 设置默认的 Django 设置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# 创建 Celery 应用
app = Celery('backend')
app.config_from_object('celery_task.config')

# 从所有已注册的应用中加载任务模块
app.autodiscover_tasks()
