from django.contrib import admin
from .models import *
from tinymce.widgets import TinyMCE


# Register your models here.
class CommentInline(admin.StackedInline):
    model = Comment
    classes = ['collapse']
    extra = 0

class PostImagesInline(admin.TabularInline):
    model = PostImages
    classes = ['collapse']
    extra = 0

@admin.register(Post)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','category','subcategory' ,'author', 'date_published', 'is_published')
    list_filter = ('category','subcategory','is_published',)
    inlines = [PostImagesInline, CommentInline]

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }

    search_fields = ['title', 'category', 'author', 'is_published']


admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(PostImages)
admin.site.register(Comment)
admin.site.register(Like)

