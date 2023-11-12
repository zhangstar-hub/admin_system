import datetime

from django.db import models


class MinuteData(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name="分组ID，一分钟一组")
    success = models.IntegerField(default=0, verbose_name="成功数量")
    failed = models.IntegerField(default=0, verbose_name="失败数量")

    @staticmethod
    def get_pid():
        """获取当前PID"""
        year_early = datetime.datetime(datetime.datetime.today().year, 1, 1)
        pid = int((datetime.datetime.now() - year_early).total_seconds() // 60) % (60 * 24 * 360)
        return pid

    class Meta:
        abstract = True


class SmsMinuteData(MinuteData):

    class Meta:
        db_table = 'sms_minute_data'


class EmailMinuteData(MinuteData):
    class Meta:
        db_table = 'email_minute_data'


class SmsData(models.Model):

    total_num = models.IntegerField(default=0, verbose_name="发送总数")
    progress_num = models.IntegerField(default=0, verbose_name="发送进度")
    failed_num = models.IntegerField(default=0, verbose_name="发送失败的数量")
    desc = models.CharField(max_length=256, default="", blank=True)

    class Meta:
        db_table = 'sms_data'
