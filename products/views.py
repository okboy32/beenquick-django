import os

from rest_framework.response import Response

from beenquickServer.settings import BASE_DIR
from django.shortcuts import render, HttpResponse
from rest_framework import mixins, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
# Create your views here.
from django.views import View

from products.models import Categorys, Products
from .tasks import xmlParser
from .serializer import CategorysSerializer, ProductsSerializer
from .filter import ProductsFilter

class uploadFormView(View):
    """
    （不属于本项目）
    面试题：ajax上传文件检测是否为excel，用celery异步解析xml文件保存
    """
    def get(self,request):
        return render(request,'upload.html')

    def post(self,request):
        file = request.FILES.get('file','')
        if file == '':
            return HttpResponse('Please choose a file')
        #验证是否是xml文件
        ext = os.path.splitext(file.name)[1]
        if ext != '.xml':
            return HttpResponse('not a xml')
        upload_dir = os.path.join(BASE_DIR,'upload')

        #是否存在uplaod目录
        if not os.path.exists(upload_dir):
            os.mkdir(upload_dir)

        #保存文件
        file_path = os.path.join(upload_dir,file.name)
        with open(file_path,'wb') as f:
            for chrunk in file.chunks():
                f.write(chrunk)

        xmlParser(file_path)
        return HttpResponse('ok')


class CategoryViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):

    queryset = Categorys.objects.filter(pcid='100002').all().order_by('sort')
    serializer_class = CategorysSerializer

class ProductsViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset = Products.objects.all().order_by('sort')
    serializer_class = ProductsSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_class = ProductsFilter
    search_fields = ('keywords','longname','specifics')
