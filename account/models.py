from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not phone:
            raise ValueError("Users must have an email address")

        user = self.model(
            phone=self.normalize_email(phone),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            phone,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="ادرس ایمیل ",
        max_length=255,
        unique=True,
        null=True,
        blank=True,
    )
    full_name = models.CharField(max_length=255, verbose_name="نام و نام خانوادگی ")
    phone = models.CharField(max_length=12, unique=True ,verbose_name='شماره موبایل')
    melicode = models.CharField(max_length=10, null=True, blank=True, verbose_name='کد ملی')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    is_admin = models.BooleanField(default=False, verbose_name='ادمین')

    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []


    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربرها'


    def __str__(self):
        return f'{self.phone} {self.full_name}'

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin



class Otp(models.Model):
    token = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=(11))
    code = models.SmallIntegerField()
    expiration_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.phone

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    full_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=300)
    postal_code = models.CharField(max_length=11)
    email = models.EmailField(null=True, blank=True)

    class Meta:
        verbose_name = 'ادرس'
        verbose_name_plural = 'ادرس ها'

    def __str__(self):
        return f'{self.full_name} - {self.phone} - {self.address[:20]}'