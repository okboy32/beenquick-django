from rest_framework import serializers
from beenquickServer.settings import REGEX_MOBILE
import re
import datetime

from users.models import VerifyCode

class SmsCodeSerializer(serializers.Serializer):

    mobile = serializers.CharField(max_length=11, min_length=11, required=True)

    def validate_mobile(self,mobile):
        """
        验证手机号码
        """
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号不合法")

        one_mintes_ago = datetime.datetime.now() - datetime.timedelta(hours=0, minutes=10, seconds=0)
        if VerifyCode.objects.filter(mobile=mobile,add_time__gt=one_mintes_ago).count():
            raise  serializers.ValidationError("验证码发送频率过快，清一分钟以后在发送")

        return mobile