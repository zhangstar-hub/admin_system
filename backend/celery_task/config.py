from datetime import timedelta

from kombu import Queue, Exchange

broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/1'
timezone = 'Asia/Shanghai'
task_serializer = 'json'
result_serializer = 'json'
broker_connection_retry_on_startup = True
task_annotations = {'celery_task.sms_task.*': {'rate_limit': '1/s'}}

task_routes = {
    'celery_task.sms_task.*': {
        'queue': 'sms'
    }
}

task_queues = (
    Queue('sms', Exchange('sms', type='direct'), routing_key='sms'),
)

beat_schedule = {
    'celery_task.sms_task.timer_send_sms': {
        'task': 'celery_task.sms_task.timer_send_sms',
        'schedule': timedelta(seconds=100),  # 每隔30秒执行一次
        'options': {'queue': 'sms'}
    },
}


