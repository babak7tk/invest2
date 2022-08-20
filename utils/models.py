from django.db import models
from django_jalali.db import models as jmodels


class CustomModel(models.Model):
    created_at = jmodels.jDateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ثبت"
    )
    updated_at = jmodels.jDateTimeField(
        auto_now=True,
        verbose_name="تاریخ ویرایش"
    )

    # created_at = models.DateTimeField(
    #     auto_now_add=True,
    #     verbose_name="تاریخ ثبت"
    # )
    # updated_at = models.DateTimeField(
    #     auto_now=True,
    #     verbose_name="تاریخ ویرایش"
    # )

    class Meta:
        abstract = True
        ordering = ['-created_at']
