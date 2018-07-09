from django.db.migrations.serializer import BaseSequenceSerializer
from rest_framework import serializers

from products.models import Categorys, Products


class ChildrenCategorysSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categorys
        fields = "__all__"


class CategorysSerializer(serializers.ModelSerializer):

    children = ChildrenCategorysSerializer(many=True)

    class Meta:
        model = Categorys
        fields = "__all__"

class ProductsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Products
        fields = ('id','img','name','partner_price','market_price','specifics','brand_name','safe_day','safe_unit')
