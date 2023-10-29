from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from system.models import User, Permission, Menu, Role


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
        exclude = ['pid']

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
