import jdatetime
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django_jalali.db import models as jmodels
from utils.validator import mobile_regex, mobile_validator, national_id_regex, \
    persian_regex
from .managers import UserManager


def upload_avatar(instance, filename):
    path = 'users/avatar/' + slugify(instance.phone, allow_unicode=True)
    return path + '/' + filename


##########################################################


class User(AbstractBaseUser, PermissionsMixin):
    firstName = models.CharField(
        max_length=100,
        null=True, blank=True,
        verbose_name="نام",
        validators=[
            RegexValidator(
                regex=persian_regex,
                message="فقط حروف فارسی مجاز است."
            )
        ]
    )
    lastName = models.CharField(
        max_length=100,
        null=True, blank=True,
        verbose_name="نام خانوادگی",
        validators=[
            RegexValidator(
                regex=persian_regex,
                message="فقط حروف فارسی مجاز است."
            )
        ]
    )
    phone = models.CharField(verbose_name="شماره موبایل", max_length=11, unique=True, validators=[mobile_regex], null=True, blank=True)

    date_joined = models.DateTimeField(verbose_name="تاریخ عضویت", default=timezone.now)
    last_login = models.DateTimeField(verbose_name="آخرین ورود", auto_now=True)

    is_superuser = models.BooleanField(verbose_name="آیا مدیر است؟", default=False)
    is_active = models.BooleanField(verbose_name="آیا فعال است؟", default=False)
    is_staff = models.BooleanField(verbose_name="آیا کارمند است؟", default=False)

    national_id = models.CharField(
        max_length=10,
        verbose_name="کد ملی",
        unique=True,
        validators=[national_id_regex],
    )

    avatar = models.ImageField(verbose_name='عکس پروفایل', null=True, blank=True, upload_to=upload_avatar)

    created_at = jmodels.jDateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ثبت"
    )
    updated_at = jmodels.jDateTimeField(
        auto_now=True,
        verbose_name="تاریخ ویرایش"
    )

    objects = UserManager()

    USERNAME_FIELD = 'national_id'
    REQUIRED_FIELDS = ['password']

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if self.phone:
            self.phone = mobile_validator(
                str(self.phone)[: 11])

        if self.phone:
            qs = User.objects.filter(
                phone=self.phone)
            if self.pk:
                qs = qs.exclude(id=self.pk)
            if qs.exists():
                raise ValidationError(
                    'شماره موبایل تکراری است و برای کاربر دیگری استفاده شده است!', code="phone")

        if self.national_id:
            qs = User.objects.filter(
                national_id=self.national_id)
            if self.pk:
                qs = qs.exclude(id=self.pk)
            if qs.exists():
                raise ValidationError(
                    'کد ملی تکراری است و برای کاربر دیگری استفاده شده است!', code="national_id")

        return super().save(*args, **kwargs)

    def get_avatar(self):
        return self.avatar.url if self.avatar else '/static/admin_panel/assets/img/avatars/default.png'

    @property
    def full_name(self):
        if self.firstName and self.lastName:
            return f"{self.firstName} {self.lastName}"
        if self.national_id:
            return self.national_id
        return self.phone or '---'