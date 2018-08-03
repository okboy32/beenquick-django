from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from django.db.models import CASCADE

from products.models import Products

User = get_user_model()

class OrderInfo(models.Model):
    """
        订单
    """
    ORDER_STATUS = (
        ("WAIT_RECEIVED", "待收货"),
        ("WAIT_COMMENT", "带评价"),
        ("AFTER_SALE", "售后中"),
        ("TRADE_FINISHED", "交易结束"),
        ("WAIT_PAY", "待付款")
    )

    user = models.ForeignKey(User, verbose_name='用户', on_delete=CASCADE)
    order_sn = models.CharField(max_length=30, null=True, blank=True, verbose_name='订单号')
    trade_no = models.CharField(max_length=30, null=True, blank=True, verbose_name='交易号')
    pay_status = models.CharField(choices=ORDER_STATUS,default="paying", max_length=20, verbose_name="订单状态")
    note = models.CharField(default="", null=True, blank=True, max_length=200, verbose_name='备注')
    order_amount = models.FloatField(default=0.0, verbose_name='订单金额')
    freight = models.FloatField(default=0.0, verbose_name='运费')
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name='支付时间')
    delivery_time = models.DateTimeField(default=datetime.now, verbose_name='送货时间')
    received_time = models.DateTimeField(null=True, blank=True, verbose_name='收货时间')

    # 用户信息
    address = models.CharField(max_length=100, default="", verbose_name='收获地址')
    signer_name = models.CharField(max_length=20, default="", verbose_name="联系人")
    signer_mobile = models.CharField(max_length=11, default="", verbose_name="联系人手机号")
    add_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')
    class Meta:
        verbose_name = '订单'
        verbose_name_plural = verbose_name

class OrderGoods(models.Model):

    order = models.ForeignKey(OrderInfo, verbose_name="订单", on_delete=CASCADE, related_name='products')
    products = models.ForeignKey(Products, verbose_name="商品", on_delete=CASCADE)
    num = models.IntegerField(default=1, verbose_name='商品数量')

    add_time = models.DateTimeField(default=datetime.now, verbose_name='创建世界')

    class Meta:
        verbose_name = "订单商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order.order_sn)