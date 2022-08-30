from django.core.validators import RegexValidator
import re
from unidecode import unidecode
from django.forms import forms
import codemelli

persian_regex = r"[1234567890۱۲۳۴۵۶۷۸۹۰آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیيئ ,._.\- -،]+"

national_id_regex = RegexValidator(
    regex=r"^[\d۱۲۳۴۵۶۷۸۹۰]{10}$",
    message="کد ملی معتبر نیست."
)

identity_number_numeric_regex = RegexValidator(
    regex=r'^([\s\d]+)$',
    message='شماره شناسنامه معتبر نیست!',
)

mobile_regex = RegexValidator(
    regex=r'(^\+?(09|98|0)?(9([0-9]{9}))$)',
    message="شماره موبایل معتبر نیست."
)

mobile_pattern = r'^\+?(09|98|0)?(9([0-9]{9}))$'


postal_code_regex = RegexValidator(
    regex=r'^(^[0-9])?$',
    message='کد پستی معتبر نیست!',
)

amount_numeric_regex = RegexValidator(
    regex=r'^([\s\d]+)$',
    message='یک عدد معتبر وارد کنید!',
)


def mobile_validator(mobile):
    if not mobile:
        return ''

    m = re.search(mobile_pattern, mobile)
    if not m:
        return ''
    mobile = '0' + str(m.group(2))
    mobile = unidecode(mobile)  # Convert to english always!
    return mobile


def national_id_validator(value):
    if not value:
        raise forms.ValidationError("کد ملی معتبر نیست.", 'national_id')

    try:
        result = codemelli.validator(value)
    except:
        raise forms.ValidationError("کد ملی معتبر نیست.", 'national_id')

    if not result:
        raise forms.ValidationError("کد ملی معتبر نیست.", 'national_id')

    return value


def validate_file_size(value):
    filesize = value.size

    if filesize > 1000 * 1024:
        raise forms.ValidationError("حداکثر حجم قابل آپلود 1 مگابایت است.")
    else:
        return value


def validate_file_required(file):
    if not file:
        raise forms.ValidationError("این فایل الزامی است.")
    return file
