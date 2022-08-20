from datetime import timedelta
import jdatetime
from django.contrib.auth import get_user_model, login
from django.db import models

# from ACL.helpers import CodeType
from utils.models import CustomModel

User = get_user_model()


class CodeManager(models.Manager):
    def create_new_code(self, user):
        from Auth.helpers import create_code

        user.codes.all().update(is_used=True)
        return Code.objects.create(code=create_code(), user=user)


class Code(CustomModel):
    code = models.CharField(verbose_name='کد', max_length=10)
    user = models.ForeignKey(verbose_name='کاربر', to=User, on_delete=models.CASCADE, related_name='codes')
    is_used = models.BooleanField(verbose_name='آیا استفاده شده است', default=False)

    class Meta:
        verbose_name = 'کد یکبار مصرف'
        verbose_name_plural = 'کد ها یکبار مصرف'

    EXPIRE_TIME = 1

    objects = CodeManager()

    def __str__(self):
        return f"{self.user}-{self.code}"

    def check_expire(self):
        expire_time = self.created_at.now() + timedelta(minutes=self.EXPIRE_TIME)
        if jdatetime.datetime.now() > expire_time:
            self.is_used = True
            self.save()
            return False
        return True

    def verify_code(self, request, is_login=False):
        self.is_used = True
        self.user.is_active = True
        self.user.save()
        self.save()

        if is_login:
            login(request, self.user)
            try:
                del request.session['verify_phone']
            except:
                pass
