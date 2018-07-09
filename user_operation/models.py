from datetime import datetime

from django.db import models
from django.db.models import CASCADE

from users.models import UserProfile
from products.models import Products
# Create your models here.

class Shopcart(models.Model):

    user = models.ForeignKey(UserProfile, verbose_name='用户', on_delete=CASCADE)
    product = models.ForeignKey(Products, verbose_name='商品', on_delete=CASCADE)
    count = models.IntegerField(default=0, verbose_name='数量')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = verbose_name