from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class UserProfile(AbstractUser):

    mobile = models.CharField(max_length=11,verbose_name='手机号')
    level = models.IntegerField(default=0)
    point = models.IntegerField(default=0)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class VerifyCode(models.Model):
    code = models.CharField(max_length=4, verbose_name='验证码')
    mobile = models.CharField(max_length=11, verbose_name="手机号")
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '短信验证码'
        verbose_name_plural = verbose_name
