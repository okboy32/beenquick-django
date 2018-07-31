from rest_framework import serializers

from user_operation.models import Shopcart
from products.serializer import ProductsShopCartSerializer


class ShopCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shopcart
        fields = ('product','count', 'selected')


class GetShopCartSeriallizer(serializers.ModelSerializer):
    product = ProductsShopCartSerializer()
    class Meta:
        model = Shopcart
        fields = ('product', 'count','selected')