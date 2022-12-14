REQUEST_STATUS_CHOICES = (
    ('1', 'ثبت موقت درخواست توسط کاربر'),
    ('10', 'در انتظار بررسی توسط مدیر'),
    ('20', 'عدم تایید درخواست | در انتظار تکمیل اطلاعات و رفع نقص'),
    ('21', 'در انتظار بررسی توسط مدیر'),
    ('30', 'تایید درخواست | در انتظار صدور کد معاملاتی بورس کالا'),
    ('40', 'تایید نهایی و صدور کد معاملاتی بورس کالا'),
    ('50', 'رد درخواست'),
)

REQUEST_STATUS_CLASS = (
    ('10', 'warning'),
    ('20', 'danger'),
    ('21', 'warning'),
    ('30', 'success'),
    ('40', 'success'),
    ('50', 'danger'),
)

USER_TYPES = (
    ('genuine', 'حقیقی'),
    ('legal', 'حقوقی'),
)

PROFESSIONAL_INVETMENT_CHOICES = (
    ('bourse', 'دارای مدرک علمی تعیین شده توسط فرابورس'),
    ('capital_market', 'کارمند ارکان بازار سرمایه'),
    ('financial_institutions', 'سابقه عضویت در هیئت مدیره نهاد های مالی'),
    ('20_transaction_value', 'حداقل ارزش معاملات 20 میلیارد ریال (طی 6 ماه اخیر)'),
    ('50_portfolio_value', 'حداقل ارزش پرتفوی 50 میلیارد ریال (طی 6 ماه اخیر)'),

    ('active_in_insurance_bank', 'فعال در بانک، بیمه و تمامی نهادهای مالی'),
    ('equity', 'حقوق صاحبان سهام سه سال آخر بیش از 100 میلیارد ریال'),
    ('average_portfolio_value', 'میانگین ارزش پرتفوی 3 سال آخر (انتهای هر ماه) بیش از 100 میلیارد ریال'),
    ('bank_account_turnover_during', 'گردش حساب بانکی طی 6 ماه اخیر (انتهای هر ماه) بیش از 100 میلیار ریال'),
)


EVIDENCE_CHOICES = (
    ('capital_markets', 'اصول بازار سرمایه'),
    ('analyst', 'تحلیلگری'),
    ('portfolio_management', 'مدیریت سبد اوراق بهادار'),
    ('securities_valuation', 'ارزشیابی اوراق بهادار'),
    ('cfa', 'تحلیلگر مالی خبره (CFA)'),
    ('frm', 'مدیریت ریسک مالی (FRM)'),
    ('cia', 'حسابرسان داخلی (CIA)'),
    ('cma', 'حسابرسی رسمی مدیریت (CMA)'),
)



REVIEW_END_PROCCESS_CHOICES = (
    ('review', 'بررسی مجدد'),
    ('end_process', 'پایان فرایند'),
)