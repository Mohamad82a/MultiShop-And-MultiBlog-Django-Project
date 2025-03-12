from django.db import models

# Create your models here.

class ShopAddress(models.Model):
    phone = models.CharField(max_length=15, verbose_name='شماره تماس')
    email = models.EmailField(verbose_name='ایمیل')
    address = models.TextField(verbose_name='ادرس')

    class Meta:
        verbose_name = "ادرس فروشگاه"
        verbose_name_plural = "ادرس فروشگاه"

    def __str__(self):
        return f'{self.phone} - {self.email} - {self.address}'