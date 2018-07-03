from datetime import datetime

from django.db import models

# Create your models here.
from django.db.models import SET_NULL, CASCADE


class Categorys(models.Model):
    name = models.CharField(max_length=10, verbose_name='类别名称')
    sort = models.IntegerField(default=0, verbose_name='排序')
    visibility = models.BooleanField(default=True, verbose_name='是否可见')
    pcid = models.ForeignKey('self',null=True,related_name='children', blank=True,on_delete=CASCADE)
    icon = models.ImageField(max_length=100, upload_to='media/upload/icons/',null=True, blank=True)
    is_open = models.BooleanField(default=True, verbose_name='is_open')
    flag = models.CharField(max_length=10, verbose_name='标识',null=True, blank=True)
    disabled_show = models.BooleanField(default=False)
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = '类别'
        verbose_name_plural = verbose_name

class Products(models.Model):
    name = models.CharField(max_length=20, verbose_name='名字')
    longname = models.CharField(max_length=200, verbose_name='长名字')
    store_nums = models.IntegerField(default=0, verbose_name='库存')
    specifics = models.CharField(max_length=50, verbose_name='规格')
    attribute = models.CharField(max_length=50, verbose_name='属性')
    sort = models.CharField(max_length=10, verbose_name='排序')
    brand_id = models.CharField(max_length=6, verbose_name='品牌编号')
    brand_name = models.CharField(max_length=10, verbose_name='简称')
    hot_degree = models.IntegerField(default=0, verbose_name='热度')
    safe_day = models.CharField(max_length=20, verbose_name='safe_day')
    safe_unit = models.CharField(max_length=10, verbose_name='safe_unit')
    market_price = models.FloatField(default=0.0, verbose_name='市场价')
    pid = models.CharField(null=True, max_length=10)
    partner_price = models.FloatField(default=0.0, verbose_name='价格')
    pre_img = models.ImageField(max_length=100, upload_to='media/upload/goods/pre_img/')
    pre_imgs = models.ImageField(max_length=100, upload_to='media/upload/goods/pre_imgs/')
    keywords = models.CharField(max_length=50, verbose_name='关键词')
    children_pid = models.CharField(max_length=10,null=True)
    cids = models.CharField(max_length=10,null=True)
    product_id = models.CharField(max_length=10, verbose_name='商品编号')
    img = models.CharField(max_length=100)

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = verbose_name