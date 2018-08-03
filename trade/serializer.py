import time
from datetime import datetime, timedelta

from rest_framework import serializers

from products.models import Products
from trade.models import OrderInfo, OrderGoods

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['img', 'id']

class OrderProductsSerializer(serializers.ModelSerializer):
    products = ProductsSerializer()
    class Meta:
        model = OrderGoods
        fields = '__all__'

class OrderInfoListSerializer(serializers.ModelSerializer):

    products = OrderProductsSerializer(many=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = OrderInfo
        fields = ['order_sn', 'id', 'order_amount', 'products', 'status','freight']

    def get_status(self, obj):
        status = obj.pay_status
        if status == 'WAIT_RECEIVED':
            status = '待收货'
        elif status == 'WAIT_COMMENT':
            status = '待评价'
        elif status == 'AFTER_SALE':
            status = '售后中'
        elif status == 'TRADE_FINISHED':
            status = '交易结束'
        elif status == 'WAIT_PAY':
            status = '待付款'
        return status

class OrderInfoSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    order_sn = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    pay_status = serializers.CharField(read_only=True)
    order_mount = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    received_time = serializers.DateTimeField(read_only=True)
    add_time = serializers.DateTimeField(read_only=True)

    def generate_order_sn(self):
        from random import Random
        random_ins = Random()
        order_sn = "{time_str}{user_id}{rand_str}".format(time_str=time.strftime('%Y%m%d%H%M%S'),
                                                          user_id=self.context['request'].user.id,
                                                          rand_str=random_ins.randint(10,99))
        return order_sn

    def validate(self, attrs):
        attrs['order_sn'] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = '__all__'
