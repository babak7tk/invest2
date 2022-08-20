import json

import requests
from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import RegexValidator
from django.contrib import messages
from django.urls import resolve
from django.contrib.auth import password_validation
from Auth.models import Code
from Sms.helpers import send_sms
from utils.validator import mobile_regex, national_id_regex, national_id_validator

User = get_user_model()


class LoginForm(AuthenticationForm):
    captcha = CaptchaField(label='کد بالا را وارد کنید')


class RegisterForm(forms.Form):
    phone = forms.CharField(
        label="شماره موبایل",
        max_length=11,
        min_length=11,
        validators=[mobile_regex],
        required=True
    )
    national_id = forms.CharField(
        max_length=10,
        min_length=10,
        label="کد ملی",
        required=True,
        validators=[national_id_regex],
    )
    captcha = CaptchaField(label='کد بالا را وارد کنید')

    class Meta:
        model = User
        fields = ['phone', 'national_id']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            qs = User.objects.filter(
                phone=phone)
            if qs.exists():
                raise forms.ValidationError('شماره موبایل تکراری است و برای کاربر دیگری استفاده شده است!', code="phone")

        return phone

    def clean_national_id(self):
        national_id = national_id_validator(self.cleaned_data.get('national_id'))
        if national_id:
            qs = User.objects.filter(
                national_id=national_id)
            if qs.exists():
                raise forms.ValidationError('کد ملی تکراری است و برای کاربر دیگری استفاده شده است!', code="national_id")

        return national_id

    def save(self):
        self.request.session['verify_phone'] = self.cleaned_data.get('phone')
        self.request.session['verify_national_id'] = self.cleaned_data.get('national_id')
        messages.success(self.request, 'کد تایید به شماره موبایل شما (ثبت شده در سامانه سجام) پیامک شد.')

    # def save(self, commit=True):
    #     user = super().save(True)
    #     # code = Code.objects.create_new_code(user)
    #
    #     # msg = f'کد تایید حساب کاربری:\n {code.code}'
    #     # sms_res = send_sms(user.phone, msg)
    #     # if not sms_res:
    #     #     raise forms.ValidationError('خطا در ارسال پیامک!', code='national_id')
    #
    #     self.request.session['verify_phone'] = user.phone
    #     self.request.session['verify_national_id'] = user.national_id
    #     messages.success(self.request, 'ثبت نام شما با موفقیت انجام شد. کد تایید حساب کاربری برای شما پیامک شد.')
    #     return user


class RegisterPasswordForm(forms.ModelForm):
    captcha = CaptchaField(label='کد بالا را وارد کنید')
    password2 = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput(), label='تکرار رمز عبور')

    class Meta:
        model = User
        fields = ['password', 'password2']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.response_data = kwargs.pop('response_data', {})
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput()

    def clean_password(self):
        password = self.cleaned_data.get('password')
        try:
            password_validation.validate_password(password, self.instance)
        except forms.ValidationError as error:
            self.add_error('password', error)
        return password

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")

        if password != password2:
            raise forms.ValidationError('رمز عبور با تکرار آن مغایرت دارد!')

        return password2

    def save(self, commit=True):
        password = self.cleaned_data.pop('password', None)
        if password:
            self.instance.set_password(password)

        instance = User.objects.create_user_request_contract(self.instance, self.response_data)
        return instance


class PasswordResetForm(forms.ModelForm):
    captcha = CaptchaField(label='کد امنیتی')
    national_id = forms.CharField(label='کد ملی', required=True, min_length=10,
                                  widget=forms.TextInput(attrs={'placeholder': 'کد ملی را وارد کنید'}),
                                  max_length=10, validators=[national_id_regex])
    phone = forms.CharField(label='شماره موبایل', required=True, min_length=11,
                            widget=forms.TextInput(attrs={'placeholder': 'شماره موبایل را وارد کنید'}),
                            max_length=11, validators=[mobile_regex])

    class Meta:
        model = Code
        fields = ['national_id', 'phone']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean(self):
        national_id_validator(self.cleaned_data.get('national_id'))

        if not User.objects.filter(phone=self.cleaned_data.get('phone'),
                                   national_id=self.cleaned_data.get('national_id')).exists():
            raise forms.ValidationError('کاربری با این مشخصات وجود ندارد!', code='national_id')

        return super().clean()

    def save(self, commit=True):
        phone = self.cleaned_data.pop('phone')
        user = User.objects.filter(phone=phone).first()

        code = Code.objects.create_new_code(user)

        msg = f'کد تایید حساب کاربری:\n {code.code}'
        sms_res = send_sms(phone, msg)
        if not sms_res:
            raise forms.ValidationError('خطا در ارسال پیامک!', code='national_id')

        self.request.session['verify_phone'] = phone
        self.request.session['verify_national_id'] = user.national_id
        messages.success(self.request, 'کد تایید حساب کاربری به شماره موبایل شما پیامک شد.')

        return code


class CodeForm(forms.Form):
    captcha = CaptchaField(label='کد امنیتی')
    code = forms.CharField(label='کد تایید', required=True, min_length=5, max_length=5, validators=[RegexValidator(
        regex=r'^-?\d+\Z',
        message="کد تایید باید عددی باشد.",
    )], widget=forms.TextInput(attrs={'placeholder': 'کد تایید دریافت شده از طریق پیامک را وارد کنید'}), )
    phone = forms.CharField(label='شماره موبایل کاربر', required=True, widget=forms.HiddenInput, min_length=11,
                            max_length=11, validators=[mobile_regex])
    national_id = forms.CharField(label='کد ملی', required=True, min_length=10,
                                  widget=forms.TextInput(attrs={'placeholder': 'کد ملی را وارد کنید'}),
                                  max_length=10, validators=[national_id_regex])

    class Meta:
        model = Code
        fields = ['code', 'phone']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean(self):
        phone = self.cleaned_data.get('phone')
        national_id = self.cleaned_data.get('national_id')
        code = self.cleaned_data.get('code')

        if not phone or not national_id:
            raise forms.ValidationError('کاربر پیدا نشد!', code='user')

        # code = Code.objects.filter(user__phone=phone, code=code, is_used=False).first()
        # if not code or not code.check_expire():
        #     raise forms.ValidationError('کد وارد شده معتبر نیست یا منقضی شده است!', code='code')

        if resolve(self.request.path_info).url_name != 'verify-register-code':
            code = Code.objects.filter(user__phone=phone, code=code, is_used=False).first()
            if not code or not code.check_expire():
                raise forms.ValidationError('کد وارد شده معتبر نیست یا منقضی شده است!', code='code')

        return self.cleaned_data

    def save(self, commit=True):
        code = None

        user = User.objects.filter(phone=self.cleaned_data['phone']).first()
        if not user:
            raise forms.ValidationError('کاربر پیدا نشد!', code='user')

        if resolve(self.request.path_info).url_name == 'password-reset-confirm':
            code = Code.objects.filter(user__phone=self.cleaned_data['phone'], code=self.cleaned_data['code']).first()
            code.verify_code(self.request, False)
            self.request.session['reset_password_code'] = code.code
            messages.success(self.request, 'رمز عبور جدید خود را وارد کنید.')
        else:
            messages.success(self.request, 'حساب کاربری شما با موفقیت ساخته شد. اکنون می‌توانید وارد شوید.')
            user.is_active = True
            user.save()
        return code


class VerifyNationalidForm(forms.Form):
    national_id = forms.CharField(
        required=False,
        min_length=10,
        max_length=10,
        label="کد ملی",
        validators=[national_id_regex],
    )

    class Meta:
        model = Code
        fields = ['national_id']
