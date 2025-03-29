from datetime import datetime

from django.urls import reverse
from django.utils import timezone
from django.db import models
from django.utils.text import slugify

from account.models import User
from tinymce import models as tinymce_models
# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name='عنوان')
    image = models.ImageField(upload_to='images/blog_categories', null=True, blank=True)
    slug = models.SlugField(max_length=120, unique=True, allow_unicode=True, null=True, blank=True)


    class Meta:
        verbose_name = 'دسته بندی مقاله'
        verbose_name_plural = 'دسته بندی های مقاله ها'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Subcategory(models.Model):
    parent = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='subcategories', null=True, blank=True)
    title = models.CharField(max_length=50, verbose_name='عنوان')
    slug = models.SlugField(max_length=120, unique=True, allow_unicode=True, null=True, blank=True)

    class Meta:
        verbose_name = 'زیر دسته بندی مقاله'
        verbose_name_plural = 'زیر دسته بندی های مقاله ها'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles', null=True, blank=True, limit_choices_to={'is_admin': True})
    title = models.CharField(max_length=100)
    body = tinymce_models.HTMLField()
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    is_published = models.BooleanField(default=False)
    date_published = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقاله ها'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class PostImages(models.Model):
    article = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/article_images', null=True, blank=True)

    def __str__(self):
        return self.article.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='replies', null=True, blank=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.post.title} | {self.user} | {self.body[:30]}'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='likes')
    liked_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user} | {self.post.title} | {self.liked_at}'




