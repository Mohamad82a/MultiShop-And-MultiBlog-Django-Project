from django.db import models

# Create your models here.

class HomeCarousel(models.Model):
    image_title = models.CharField(max_length=100, verbose_name='نام عکس')
    image = models.ImageField(upload_to='homecarousel', verbose_name='عکس')

    class Meta:
        verbose_name = 'عکس صفحه اصلی'
        verbose_name_plural = 'عکس های صفحه اصلی'

    def __str__(self):
        return self.image_title

class UnderCarousel(models.Model):
    image_title = models.CharField(max_length=100, verbose_name='نام عکس')
    image = models.ImageField(upload_to='homecarousel', verbose_name='عکس')

    class Meta:
        verbose_name = 'عکس جانبی صفحه'
        verbose_name_plural = 'عکس های جانبی صفحه'

    def __str__(self):
        return self.image_title