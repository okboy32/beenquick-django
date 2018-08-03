from datetime import datetime, timedelta

from django.shortcuts import render
from rest_framework import mixins, viewsets, status
# Create your views here.
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from user_operation.models import Shopcart
from .serializer import OrderInfoSerializer, OrderInfoListSerializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from unit.permissions import IsOwnerOrReadOnly
from .models import OrderInfo, OrderGoods


class OrderInfoViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = OrderInfo.objects.all()
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_serializer_class(self):
        if self.action is 'list':
            return OrderInfoListSerializer
        else:
            return OrderInfoSerializer

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        if isinstance(request.data['delivery_time'],int):
            hour = datetime.now().hour
            delhour = request.data['delivery_time']
            if ((hour + delhour) % 24) >= 9 or  ((hour + delhour) % 24) <= 23:
                request.data['delivery_time'] = datetime.now() + timedelta(hours=delhour)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ret = self.perform_create(serializer)
        if ret is not None:
            return ret
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        shop_carts = Shopcart.objects.filter(user=self.request.user, selected=True).all()
        shop_carts = [shop_cart for shop_cart in shop_carts]
        amount = 0
        local_shopcart = self.request.data.get('shopcart', None)
        if local_shopcart is None:
            return Response({
                'shopcart':'参数错误'
            }, status=status.HTTP_400_BAD_REQUEST, headers={})
        for shop_cart in shop_carts:
            if local_shopcart[str(shop_cart.product.id)] is not shop_cart.count:
                return Response({
                    'shopcart': '参数错误'
                }, status=status.HTTP_400_BAD_REQUEST, headers={})
            amount += shop_cart.count * shop_cart.product.partner_price
        order_amount = self.request.data['order_amount']
        if amount != order_amount:
            return Response({
                'order_amount': '参数错误'
            }, status=status.HTTP_400_BAD_REQUEST, headers={})
        order = serializer.save()
        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.products = shop_cart.product
            order_goods.num = shop_cart.count
            order_goods.order = order
            order_goods.save()
            shop_cart.delete()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)