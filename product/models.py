from django.db import models
from django.db.models import SET_NULL
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone

from account.models import User
from tinymce import models as tinymce_models
from django import forms


# Create your models here.


class Category(models.Model):
    # parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, related_name='subcategories')
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)
    slug = models.SlugField(max_length=120, unique=True, allow_unicode=True)

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.title

class Subcategory(models.Model):
    parent = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, unique=True, allow_unicode=True)

    class Meta:
        verbose_name = 'زیر دسته بندی'
        verbose_name_plural = 'زیر دسته بندی ها'

    def __str__(self):
        return self.title


class Product(models.Model):
    class Status(models.TextChoices):
        is_available = 'available', 'موجود'
        unavailable = 'unavailabe', 'ناموجود'

    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, null=True, blank=True, verbose_name='دسته بندی محصول')
    subcategory = models.ForeignKey(Subcategory, related_name='products', on_delete=models.CASCADE, null=True, blank=True, verbose_name='زیر دسته بندی محصول')
    title = models.CharField(max_length=100, verbose_name='نام محصول')
    description = tinymce_models.HTMLField(verbose_name='توضیحات')
    price = models.BigIntegerField(verbose_name='قیمت')
    discount = models.BigIntegerField(default=0, verbose_name='تخفیف')
    discount_expiray = models.DateTimeField(null=True, blank=True, verbose_name='انقضای تخفیف')
    discount_price = models.BigIntegerField(default=0, verbose_name='قیمت با تخفیف')
    discount_percentage = models.BigIntegerField(null=True, blank=True, verbose_name='درصد تخفیف')
    is_discount_active = models.BooleanField(default=False, verbose_name='فعال؟')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.unavailable, verbose_name='وضعیت')
    slug = models.SlugField(max_length=255, null=True, blank=True, verbose_name='اسلاگ')
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product:product_detail', kwargs={'pk': self.id,'slug': self.slug})

    def update_discount(self):

        if self.discount > 0 :
            self.discount_price = self.price - self.discount
            self.discount_percentage = max(1, round((self.discount / self.price) * 100))

        else:
            self.discount_price = self.price
            self.discount_percentage = 0
        self.save()

    def is_discount_valid(self):
        return self.discount > 0 and self.discount_expiry and self.discount_expiry > timezone.now()

    def remove_discount(self):
        if not self.is_discount_valid():
            self.discount = 0
            self.discount_price = self.price
            self.discount_expiry = None
            self.save()

    def __str__(self):
        return self.title


### Features For Products ###

class Attribute(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='attributes')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE ,null=True, blank=True)
    name = models.CharField(max_length=225)

    class Meta:
        verbose_name = 'ویژگی'
        verbose_name_plural = 'ویژگی ها'

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attribute_values', null=True, blank=True)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='attribute_values')
    value = models.CharField(max_length=225)

    class Meta:
        verbose_name = 'مقدار ویژگی'
        verbose_name_plural = 'مقدار های ویژگی ها'

    def __str__(self):
        return self.value




class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='عکس محصول')
    # image fields
    image = models.ImageField(upload_to='product_images/', null=True, blank=True, verbose_name='عکس')

    class Meta:
        verbose_name = 'عکس های محصول '
        verbose_name_plural = 'عکس های محصولات'

    def __str__(self):
        return self.product.title

class Speculation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='spec')
    text = tinymce_models.HTMLField()

    class Meta:
        verbose_name = 'مشخصات کالا'
        verbose_name_plural = 'مشخصات کالا ها'

    def __str__(self):
        return self.text[:30]


# class SpecForm(forms.ModelForm):
#     class Meta:
#         model = Spectaculation, Product
#         fields = ['test', 'description']
#         widgets = {
#             'content': WYSIWYGWidget(),
#         }

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')
    liked_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'مورد علاقه'
        verbose_name_plural = 'مورد علاقه ها'
        unique_together = ('user', 'product')

    def __str__(self):
        return f'{self.user.full_name} | {self.product.title} | {self.liked_at}'