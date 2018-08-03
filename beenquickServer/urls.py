"""beenquickServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

from products.views import uploadFormView, CategoryViewSet, ProductsViewSet
from rest_framework_jwt.views import obtain_jwt_token
from trade.views import OrderInfoViewSet
from users.views import SmsCodeViewSet, UserViewSet
from user_operation.views import ShopcartViewSet

router = DefaultRouter()

#短信验证码接口
router.register(r'codes', SmsCodeViewSet, base_name='codes')
#商品类别接口
router.register(r'category', CategoryViewSet, base_name='category')
#商品接口
router.register(r'products',ProductsViewSet, base_name='products')
#用户接口
router.register(r'user',UserViewSet, base_name="user")
#购物车借口
router.register(r'shopcart',ShopcartViewSet, base_name="shopcart")
#订单接口
router.register(r'order', OrderInfoViewSet, base_name='order')

from .views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    url('upload/',uploadFormView.as_view(),name='upload'),
    url(r'^api/',include(router.urls)),

    #配置django API 文档
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'docs/', include_docs_urls(title='爱鲜蜂')),
    url(r'^api/login/', obtain_jwt_token),

    #配置app页面
    url(r'^', index)
]
