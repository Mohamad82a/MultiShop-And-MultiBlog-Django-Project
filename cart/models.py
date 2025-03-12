from datetime import timedelta
from django.db import models
from django.utils.timezone import now

from account.models import User
from product.models import Product, AttributeValue, Attribute
from account.models import Address
from django_jalali.db import models as jmodels

# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders',verbose_name='کاربر')
    address = models.ForeignKey(Address,null=True, blank=True, on_delete=models.CASCADE)
    item_quantities = models.IntegerField(default=0, verbose_name='مجموع تعداد محصولات')
    total_price = models.BigIntegerField(default=0, verbose_name='قیمت کلی محصولات')
    order_date = jmodels.jDateField(auto_now_add=True,verbose_name='تاریخ سفارش')
    is_paid = models.BooleanField(default=False, verbose_name='وضعیت پرداخت')


    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش ها'

    def __str__(self):
        return f'{self.user.full_name}-{self.user.phone}-{self.order_date}-{self.is_paid}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items', verbose_name='سفارش')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items', verbose_name='محصول')
    attribute = models.JSONField(default=dict, verbose_name='مشخصات کالا')
    quantity = models.IntegerField(verbose_name='تعداد')
    price = models.BigIntegerField(verbose_name='قیمت')

    class Meta:
        verbose_name = 'کالا های موجود در سفارش'
        verbose_name_plural = 'کالا های موجود در سفارش ها'

    def __str__(self):
        return f'{self.order.user.phone} - {self.product.title}'


def add_30_days():
    return now() + timedelta(days=30)

class DiscountCode(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name='کد تخفیف')
    discount = models.DecimalField(max_digits=5,decimal_places=2, verbose_name='درصد تخفیف')
    quantity = models.SmallIntegerField(default=0, verbose_name='تعداد کد')
    valid_from = models.DateTimeField(default=now)
    valid_to = models.DateTimeField(default=add_30_days)
    is_used = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'کد تخفیف'
        verbose_name_plural = 'کد های تخفیف'

    def __str__(self):
        return self.code

class UserDiscountCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    discount_code = models.ForeignKey(DiscountCode, on_delete=models.CASCADE)
    used_at = models.DateTimeField(auto_now_add=True)
    overall_discount = models.BigIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'discount_code')


    def __str__(self):
        return f'{self.user} - {self.discount_code}'