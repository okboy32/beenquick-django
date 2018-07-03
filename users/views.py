import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.shortcuts import render
from rest_framework import mixins, viewsets, status, authentication
from rest_framework.response import Response
import random
import json
# Create your views here.
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from users.models import VerifyCode, UserProfile
from users.serializers import SmsCodeSerializer
from unit.alidayu_send_sms import send_sms

User = get_user_model()

class SmsCodeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    获取验证码
    """
    serializer_class = SmsCodeSerializer
    @staticmethod
    def generate_code():
        str_seed = '1234567890'
        return ''.join([random.choice(str_seed) for _ in range(0, 4)])


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        #生成验证码
        params = {}

        mobile = serializer.validated_data['mobile']
        code = self.generate_code()

        params['code'] = code
        params['product'] = 'mshop'
        params = json.dumps(params)
        #发送验证码
        ret = send_sms(mobile,template_param=params)
        ret = str(ret,encoding='utf-8')
        ret = json.loads(ret)

        if ret['Code'] == 'OK':
            #向数据添加验证码
            code_record = VerifyCode(code=code,mobile=mobile)
            code_record.save()

            #用户是否存在，不存在则创建
            if not UserProfile.objects.filter(mobile=mobile).first():
                user = UserProfile()
                user.mobile = mobile
                user.username = mobile
                user.name = mobile
                user.save()
            return Response({
                'mobile':mobile
            },status=status.HTTP_201_CREATED)
        else:
            return Response({
                'mobile': ret['Message']
            },status=status.HTTP_400_BAD_REQUEST)

class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            five_mintes_ago = datetime.datetime.now() - datetime.timedelta(hours=0, minutes=5, seconds=0)
            user = VerifyCode.objects.filter(mobile=username, add_time__gt=five_mintes_ago,code=password).first()
            if user:
                user = User.objects.get(mobile=user.mobile)
                return user
        except Exception as e:
            return None


