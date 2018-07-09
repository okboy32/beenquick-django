from django.shortcuts import render
from rest_framework import mixins, viewsets, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from user_operation.models import Shopcart
from user_operation.serializer import ShopCartSerializer
from unit.permissions import IsOwnerOrReadOnly
# Create your views here.

class ShopcartViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Shopcart.objects.all()
    serializer_class = ShopCartSerializer
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return Shopcart.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        count = serializer.validated_data.get('count')
        product = serializer.validated_data.get('product')
        if count and product:
            record = Shopcart.objects.filter(user=request.user,product=product).first()
            if record:
                record.count += count
                if record.count > 0:
                    record.save()
                    return Response({
                        "count": record.count,
                        "product": product.id
                    }, status=status.HTTP_201_CREATED)
                else:
                    record.delete()
                    return Response({
                        "count": 0,
                        "product": product.id
                    }, status=status.HTTP_201_CREATED)
            else:
                if count >= 1:
                    shopcard = Shopcart(count=1,user=request.user,product=product)
                    shopcard.save()
                    return Response({
                        "count": shopcard.count,
                        "product": shopcard.product
                    }, status=status.HTTP_201_CREATED)
        return Response({
            "msg":"缺少参数或者参数有误"
        },status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save()