from rest_framework import serializers

from user_operation.models import Shopcart


class ShopCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shopcart
        fields = ('product','count')