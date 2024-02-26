# django后台管理系统

## 概述

这个代码是一个后台模板，包括一些基础的功能，如下：

1. 登陆功能
2. 基于角色的权限管理
3. celery分布式任务调用

使用的主要技术django restframework+celery+redis+gunicorn，使用的基本包基本都是框架自带的，比较简单一点。

## 快速开始

### 先决条件

- Python (>=3.x)
- Django

### 目录结构

​	-- backend	# django默认目录

​	-- celery_task	# celery 配置和任务，分布式/后台任务会用到

​	-- config	# 放配置和配置模板的地方

​	-- logs	# log 存放地

​	-- static	# django静态文件

​	-- system	# 创建的后台系统app，主要的代码都在里面

​	-- tmp	# 临时文件目录，主要放是pid文件	

​	-- utils	# 一些工具代码存放地

​	celery.sh 	# celery 启动脚本

​	gunicorn.sh	# gunicorn 启动脚本，django启动全靠他 

### 安装

1. 设置运行环境：

   ```bash
   python -m venv env
   pip install -r requirements.txt

​		修改config/gunicorn_config.py文件

​		chdir: 自己代码所在位置

2. 运行

​		启动django程序： sh gunicorn.sh start

​		启动celery：sh celery.sh start

3. 需要自己设置登录账号密码
   
      python manage.py createsuperuser
      
