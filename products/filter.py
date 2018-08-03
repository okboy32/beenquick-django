import django_filters

from products.models import Products


class ProductsFilter(django_filters.rest_framework.FilterSet):

    #name = django_filters.CharFilter(name='name',lookup_expr='icontains')

    class Meta:
        model = Products
        fields = ['pid']