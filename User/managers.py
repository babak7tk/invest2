from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, national_id, password, **extra_fields):
        if not national_id:
            raise ValueError('The given phone must be set')

        user = self.model(national_id=national_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, national_id, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(national_id, password, **extra_fields)

    def create_superuser(self, national_id, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(national_id, password, **extra_fields)
