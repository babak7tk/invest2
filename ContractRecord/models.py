import os

import requests
from PIL import Image
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
from utils.validator import national_id_regex
from ContractRecord.helpers import *
from ContractRecord.mixins import ContactRequestLoggerMixin
from config.settings import MEDIA_ROOT
from utils.models import CustomModel
from utils.validator import mobile_regex, validate_file_size, persian_regex, postal_code_regex, amount_numeric_regex

User = get_user_model()


def upload_files(instance, filename):
    n_id = slugify(instance.national_id, allow_unicode=True)
    return 'requests/' + n_id + '/' + filename

##########################################################

class ContactRequest(CustomModel):
    national_id = models.CharField(
        max_length=10,
        verbose_name="کد ملی",
        validators=[national_id_regex],
    )

    user_type = models.CharField(
        max_length=200,
        verbose_name="نوع شخص",
        choices=USER_TYPES
    )

    professional_investment = models.CharField(
        max_length=200,
        verbose_name="نوع سرمایه گذاری حرفه ای",
        choices=PROFESSIONAL_INVETMENT_CHOICES
    )

    financial_institutions_status = models.CharField(
        max_length=200,
        verbose_name="وضعیت سابقه عضویت در هیئت مدیره نهاد های مالی",
        default='end_process',
        choices=REVIEW_END_PROCCESS_CHOICES
    )

    transaction_value_status = models.CharField(
        max_length=200,
        verbose_name="وضعیت حداقل ارزش معاملات 20 میلیارد ریال",
        default='end_process',
        choices=REVIEW_END_PROCCESS_CHOICES
    )

    portfolio_value_status = models.CharField(
        max_length=200,
        verbose_name="وضعیت حداقل ارزش پرتفوی 50 میلیارد ریال",
        default='end_process',
        choices=REVIEW_END_PROCCESS_CHOICES
    )

    legal_category_status = models.CharField(
        max_length=200,
        verbose_name="وضعیت دسته بندی حقوقی سرمایه گذار",
        default='end_process',
        choices=REVIEW_END_PROCCESS_CHOICES
    )

    """ Files """
    capital_markets_file = models.FileField(
        verbose_name='مدرک اصول بازار سرمایه', null=True, blank=True,
        upload_to=upload_files,
        validators=[
            # FileExtensionValidator(['jpg', 'jpeg', 'png', 'bmp']),
            validate_file_size
        ],
    )

    analyst_file = models.FileField(
        verbose_name='مدرک تحلیلگری',
        null=True, blank=True,
        upload_to=upload_files,
        validators=[
            validate_file_size
        ],
    )

    portfolio_management_file = models.FileField(
        verbose_name='مدرک مدیریت سبد اوراق بهادار',
        null=True, blank=True,
        upload_to=upload_files,
        validators=[
            validate_file_size
        ],
    )

    securities_valuation_file = models.FileField(
        verbose_name='مدرک ارزشیابی اوراق بهادار', null=True, blank=True, upload_to=upload_files,
        validators=[
            validate_file_size
        ],
    )

    cfa_file = models.FileField(
        verbose_name='مدرک تحلیلگر مالی خبره (CFA)', null=True, blank=True, upload_to=upload_files,
        validators=[
            validate_file_size
        ],
    )

    frm_file = models.FileField(
        verbose_name='مدرک مدیریت ریسک مالی (FRM)', null=True, blank=True, upload_to=upload_files,
        validators=[
            validate_file_size
        ],
    )

    cia_file = models.FileField(
        verbose_name='مدرک حسابرسان داخلی (CIA)', null=True, blank=True, upload_to=upload_files,
        validators=[
            validate_file_size
        ],
    )

    cma_file = models.FileField(
        verbose_name='مدرک حسابرسی رسمی مدیریت (CMA)', null=True, blank=True, upload_to=upload_files,
        validators=[
            validate_file_size
        ],
    )

    insurance_report_file = models.FileField(
        verbose_name='مدرک گزارش سایقه بیمه', null=True, blank=True, upload_to=upload_files,
        validators=[
            validate_file_size
        ],
    )

    account_circulation_report_file = models.FileField(
        verbose_name='فایل گزارش گردش حساب', null=True, blank=True, upload_to=upload_files,
        validators=[
            validate_file_size
        ],
    )

    req_status = models.CharField(
        verbose_name='وضعیت', max_length=255, choices=REQUEST_STATUS_CHOICES, default='1',
        null=True, blank=True
    )

    class Meta:
        verbose_name = 'اطلاعات درخواست'
        verbose_name_plural = 'اطلاعات درخواست‌ها'

    def __str__(self):
        return self.national_id

    # Create final user request pdf from uploaded files

    def create_final_pdf(self):
        images = []
        base_pdf = None

        # PDF path and directory create
        pdf_name = slugify(self.user.national_id,
                           allow_unicode=True) + '_final.pdf'
        pdf_path = os.path.join(MEDIA_ROOT, 'requests', 'final_pdf')
        if not os.path.exists(pdf_path):
            os.mkdir(pdf_path)
        pdf_path += '/' + pdf_name

        # get uploaded files path from database
        for item in ['signature_image', 'birth_certificate_image_1', 'birth_certificate_image_2',
                     'birth_certificate_image_3', 'national_card_image_front', 'national_card_image_back',
                     'business_license_image',
                     'tax_system_registration_image',
                     'comprehensive_registration_image',
                     'national_smart_card_image']:
            if getattr(self, item):
                current_image = Image.open(getattr(self, item))
                current_image = current_image.convert('RGB')
                if not base_pdf:
                    base_pdf = current_image
                else:
                    images.append(current_image)

        # save the output to final pdf file
        if base_pdf and len(images) > 0:
            base_pdf.save(pdf_path, save_all=True, append_images=images)
            self.final_pdf = os.path.join(
                'requests', 'final_pdf') + '/' + pdf_name
            super().save()

    @property
    def get_req_status(self):
        return dict(REQUEST_STATUS_CHOICES).get(self.req_status, '')

    @property
    def get_req_status_class(self):
        return dict(REQUEST_STATUS_CLASS).get(self.req_status, '')
