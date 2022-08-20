from django.contrib import messages
from django.core.validators import RegexValidator
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from Auth.helpers import create_code
from Auth.models import Code
from Sms.helpers import send_sms
from utils.validator import mobile_regex

User = get_user_model()


class CodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6, min_length=6, required=False, validators=[RegexValidator(
        regex=r'^-?\d+\Z',
        message="کد تایید باید عددی باشد",
    )])
    phone = serializers.CharField(max_length=11, min_length=11, required=True, validators=[mobile_regex])

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def save(self, **kwargs):
        phone = self.validated_data.get('phone')

        user = User.objects.filter(phone=phone).first()
        if not user:
            raise serializers.ValidationError('کاربری با این شماره موبایل وجود ندارد!', code='phone')

        code = Code.objects.create_new_code(user)

        msg = f'کد تایید حساب کاربری:\n {code.code}'
        sms_res = send_sms(user.phone, msg)
        if not sms_res:
            raise serializers.ValidationError('خطا در ارسال پیامک!', code='national_id')

        self.request.session['verify_phone'] = user.phone
        self.request.session['verify_national_id'] = user.national_id
        return code


class RegisterCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6, min_length=6, required=False, validators=[RegexValidator(
        regex=r'^-?\d+\Z',
        message="کد تایید باید عددی باشد",
    )])
    phone = serializers.CharField(max_length=11, min_length=11, required=True, validators=[mobile_regex])
    national_id = serializers.CharField(
        max_length=10,
        min_length=10,
        label="کد ملی",
        required=True,
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def save(self, **kwargs):
        self.request.session['verify_phone'] = self.validated_data.get('phone')
        self.request.session['verify_national_id'] = self.validated_data.get('national_id')