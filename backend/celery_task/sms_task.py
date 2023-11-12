import random
import time

from celery import Task
from django.db import transaction
from django.db.models import F

from system.models.monitor import SmsMinuteData, SmsData
from . import app


class SmsMonitorTask(Task):
    model_class = SmsMinuteData

    def on_success(self, retval, task_id, args, kwargs):
        pid = self.model_class.get_pid()
        data, _ = self.model_class.objects.get_or_create(id=pid)
        data.success += 1
        data.save()

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        pid = self.model_class.get_pid()
        data, _ = self.model_class.objects.get_or_create(id=pid)
        data.failed += 1
        data.save()


class SmsManualTask(SmsMonitorTask):

    def on_success(self, retval, task_id, args, kwargs):
        super().on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        super().on_failure(exc, task_id, args, kwargs, einfo)
        SmsData.objects.filter(id=args[0]).update(
            progress_num=F('progress_num') + 1, failed_num=F('failed_num') + 1
        )


@app.task(base=SmsMonitorTask)
def timer_send_sms():
    time.sleep(1)
    if random.randint(1, 100) <= 2:
        raise ValueError
    print(f"send sms..")


@app.task
def send_batch_sms(mid, num):
    for i in range(num):
        manual_send_sms.apply_async(args=(mid, i))
    print("end send_batch_sms")


@app.task(base=SmsManualTask)
@transaction.atomic
def manual_send_sms(mid, i):
    time.sleep(1)
    if random.randint(1, 100) <= 2:
        raise ValueError
    print(f"send sms...{i}")
    SmsData.objects.filter(id=mid).update(progress_num=F("progress_num") + 1)
