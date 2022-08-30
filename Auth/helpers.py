import random
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import Q
from datetime import datetime, timedelta
from django.utils import timezone

from Auth.models import Code

User = get_user_model()


def check_user_exist(new_phone):
    if User.objects.filter(phone=new_phone).exists():
        raise ValidationError([
            ValidationError('این شماره موبایل قبلا ثبت شده است!', code='phone'),
        ])


def check_reset_password_sent(user):
    reset_password = user.password_resets.last()
    if reset_password:
        today = timezone.now()
        expiration = reset_password.created_at + timedelta(minutes=1)

        if today > expiration:
            return True

        return False

    return True


def check_reset_password_code_expiration(code):
    reset_password = PasswordReset.objects.filter(code=code).first()
    if reset_password and not reset_password.is_used:
        today = timezone.now()
        expiration = reset_password.created_at + timedelta(minutes=1)

        if today > expiration:
            return False

        return True

    return False


def check_login_code_sent(user):
    login_code = user.login_codes.last()
    if login_code:
        today = timezone.now()
        expiration = login_code.created_at + timedelta(minutes=1)

        if today > expiration:
            return True

        return False

    return True


def check_code_expiration(code):
    code = Code.objects.filter(code=code).first()
    if code and not code.is_used:
        today = timezone.now()
        expiration = code.created_at + timedelta(minutes=1)

        if today > expiration:
            return False

        return True

    return False


def create_code():
    try:
        return ''.join([str(random.randint(0, 9)) for item in range(6)])
    except:
        return '123456'


def check_service_response_error(response):
    if response.status_code in [500, 503]:
        raise forms.ValidationError('خطا در دریافت اطلاعات. لطفا دوباره امتحان کنید.')