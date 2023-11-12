import datetime

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from celery_task.sms_task import send_batch_sms
from system.models import SmsMinuteData, SmsData
from rest_framework.viewsets import GenericViewSet
from system.permission import RouterNameMeta
from system.serializers import SmsMinuteDataSerializer, SmsSerializer


class SmsMonitorView(ListModelMixin, GenericViewSet, metaclass=RouterNameMeta):
    router_name = 'sms_monitor'
    router_desc = "短信数据统计"
    queryset = SmsMinuteData.objects.all()
    serializer_class = SmsMinuteDataSerializer

    def list(self, request, *args, **kwargs):
        serializer = SmsMinuteDataSerializer(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)
        time_span = serializer.get_time_span(serializer.validated_data)
        data = serializer.get_data_by_span(time_span)
        year_early = serializer.get_year_early()
        datetime_span = [
            (year_early + datetime.timedelta(minutes=i)).strftime("%Y-%m-%d %H:%M") for i in time_span
        ]
        ret = {
            'datetime_span': datetime_span, 'data': data,
        }
        return Response(ret)


class SmsView(ModelViewSet, metaclass=RouterNameMeta):
    router_name = 'sms'
    router_desc = "短信发送"
    queryset = SmsData.objects.all()
    serializer_class = SmsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        send_batch_sms.apply_async(args=(serializer.instance.id, serializer.instance.total_num))
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["POST"])
    def live_show(self, request):
        id_list = self.request.data.get("id_list", [])
        ret = SmsData.objects.filter(id__in=id_list).values("id", "progress_num", "failed_num")
        return Response(ret)
