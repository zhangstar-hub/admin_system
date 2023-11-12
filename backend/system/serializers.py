import datetime

from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from system.models import User, Permission, Menu, Role, SmsMinuteData, SmsData


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ['is_superuser']

    @staticmethod
    def validate_password(password):
        return make_password(password)

    @staticmethod
    def get_permissions(user: User):
        permissions = set()
        for i in user.roles.all():
            permissions.update(i.permissions.all().values_list('id', flat=True))
        return list(permissions)


class MenuSerializer(serializers.ModelSerializer):

    children = serializers.SerializerMethodField(source='id')

    class Meta:
        model = Menu
        fields = '__all__'

    def get_children(self, data):
        children = self.Meta.model.objects.filter(pid=data.id)
        return MenuSerializer(children, many=True).data


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = '__all__'


class SmsMinuteDataSerializer(serializers.ModelSerializer):
    max_node = 60

    left_time = serializers.DateTimeField(
        write_only=True, format='%Y-%m-%d %H:%M', required=False
    )
    right_time = serializers.DateTimeField(
        write_only=True, format='%Y-%m-%d %H:%M', required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.raw_data = {}

    class Meta:
        model = SmsMinuteData
        fields = '__all__'
        read_only_fields = ['id', 'success', 'failed']

    def validate_left_time(self, value):
        value = value.replace(tzinfo=None)
        year_early = self.get_year_early()
        value = max(int((value - year_early).total_seconds()) // 60, 0)
        return value

    def validate_right_time(self, value):
        value = value.replace(tzinfo=None)
        year_early = self.get_year_early()
        value = max(int((value - year_early).total_seconds()) // 60, self.max_node)
        return value

    def validate(self, attrs):
        pid = SmsMinuteData.get_pid()
        attrs.setdefault('left_time', pid - self.max_node)
        attrs.setdefault('right_time', pid + 1)
        r_time, l_time = attrs['right_time'], attrs['left_time']
        if r_time <= l_time or r_time - l_time < 1:
            raise ValidationError(detail="时间区间选择错误")
        year_early = self.get_year_early()
        self.raw_data['left_time'] = year_early + datetime.timedelta(minutes=l_time)
        self.raw_data['right_time'] = year_early + datetime.timedelta(minutes=r_time)
        return attrs

    @staticmethod
    def get_time_span(attr):
        r_time, l_time = attr['right_time'], attr['left_time']
        span = max((r_time - l_time) // 60, 1)
        return list(range(l_time, r_time + span - 1, span))

    @staticmethod
    def get_data_by_span(time_span):
        data = []
        span = time_span[1] - time_span[0]
        for i in time_span:
            data.append({'success': 0, 'failed': 0})
            rows = SmsMinuteData.objects.filter(id__gt=i - span, id__lte=i).values('success', 'failed')
            for j in rows:
                data[-1]['success'] += j['success']
                data[-1]['failed'] += j['failed']
        return data

    @staticmethod
    def get_year_early():
        return datetime.datetime(datetime.datetime.today().year, 1, 1)


class SmsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SmsData
        fields = '__all__'
