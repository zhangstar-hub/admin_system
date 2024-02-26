import multiprocessing

bind = '0.0.0.0:8000'  // 绑定的端口
workers = multiprocessing.cpu_count() * 2 + 1
backlog = 512
chdir = '/Users/zhangxingxing/admin_system/backend'  // 文件路径
timeout = 60
max_requests = 1000
worker_connections = 1000
daemon = True
threads = 2
loglevel = 'info'
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'
accesslog = "logs/gunicorn.log"
errorlog = "logs/gunicorn.log"
pidfile = "tmp/gunicorn.pid"
pythonpath = "env/bin/python"
