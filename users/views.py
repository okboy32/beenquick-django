import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework import mixins, viewsets, status, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
import random
import json

from beenquickServer.settings import REGEX_MOBILE
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from users.models import VerifyCode, UserProfile
from users.serializers import SmsCodeSerializer, UserSerializer
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
                user.set_password('123456')
                user.save()
            return Response({
                'mobile':mobile
            },status=status.HTTP_201_CREATED)
        else:
            return Response({
                'mobile': ret['Message']
            }, status=status.HTTP_400_BAD_REQUEST)


class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(mobile=username))
            if user.check_password(password):
                return user
            import re
            if re.match(REGEX_MOBILE,username):
                user_login_by_mobile = User.objects.filter(mobile=username).first()
                five_mins_age = datetime.datetime.now() - datetime.timedelta(minutes=5)
                code = VerifyCode.objects.filter(mobile=username, add_time__gt=five_mins_age).order_by('-add_time').first()
                if code.code == password and code and user_login_by_mobile:
                    return user_login_by_mobile
        except Exception as e:
            return None


class UserViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []

        return []

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if kwargs['pk'] != str(request.user.id):
            return Response({
                'user':'无法获取他人资料'
            },status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)