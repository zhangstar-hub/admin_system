from django.db import models
from django.contrib.auth.models import AbstractUser


class Menu(models.Model):
    """
    菜单
    """
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30, unique=True, verbose_name="菜单名")
    title = models.CharField(max_length=128, null=True, blank=True, verbose_name="菜单标题")
    pid = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, verbose_name="父菜单")
    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '菜单'
        verbose_name_plural = verbose_name
        ordering = ['id']


class Permission(models.Model):
    """
    权限
    """
    name = models.CharField(max_length=30, verbose_name="权限名")
    method = models.CharField(max_length=50, null=True, blank=True, verbose_name="方法")
    menus = models.ManyToManyField("Menu", blank=True, verbose_name="菜单")
    desc = models.CharField(max_length=50, blank=True, null=True, verbose_name="描述")
    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '权限'
        verbose_name_plural = verbose_name
        ordering = ['id']
        unique_together = ('name', 'method')


class Role(models.Model):
    """
    角色
    """
    name = models.CharField(max_length=32, unique=True, verbose_name="角色")
    permissions = models.ManyToManyField("Permission", blank=True, verbose_name="权限")
    desc = models.CharField(max_length=50, blank=True, null=True, verbose_name="描述")

    class Meta:
        verbose_name = "角色"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class User(AbstractUser):
    """用户"""
    name = models.CharField(max_length=20, default="", verbose_name="姓名")
    mobile = models.CharField(max_length=11, default="", verbose_name="手机号码")
    image = models.ImageField(upload_to="static/%Y/%m", default="image/default.png",
                              max_length=100, null=True, blank=True)
    roles = models.ManyToManyField("Role", verbose_name="角色", blank=True)
    disabled_permission = models.ManyToManyField("Permission", verbose_name="禁用的权限", blank=True)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.username

    def get_user_permissions(self, obj=None):
        """用户的全部权限"""
        permissions = set()
        for i in self.roles.all():
            permissions.update(i.permissions.all().values_list('id', flat=True))
        permissions -= set(self.disabled_permission.all().values_list('id', flat=True))
        return list(permissions)

    def get_user_menus(self):
        """用户可展示的菜单"""
        permissions_id = self.get_user_permissions()
        menus = Permission.objects.filter(id__in=set(permissions_id)).values_list('menus', flat=True)
        return set(menus)
