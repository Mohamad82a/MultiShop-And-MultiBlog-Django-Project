from django.contrib import admin
from django.template.defaultfilters import title

from .models import *

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    # prepopulated_fields = {'slug': ('title',)}

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('parent',)
    search_fields = ('title','parent',)


class SpecInline(admin.StackedInline):
    model = Speculation
    classes = ['collapse']
    extra = 1
class ImageInline(admin.StackedInline):
    model = ProductImage
    classes = ['collapse']
    extra = 1

class AttributeValueTable(admin.TabularInline):
    model = AttributeValue
    autocomplete_fields = ['product','attribute']
    classes = ['collapse']
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title','id','category', 'price','discount_price','discount_percentage' ,'status',)
    autocomplete_fields = []
    inlines = (AttributeValueTable,SpecInline,ImageInline,)

    list_filter = ('category','status','subcategory',)
    search_fields = ('title','slug',)



@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    search_fields = ['name', 'category']
    list_filter = ('category',)
    inlines = (AttributeValueTable,)

@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = [ 'attribute', 'value']
    autocomplete_fields = ['attribute','product']
    search_fields = ['attribute__name', 'value']
    list_filter = ['attribute__category',]

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product_name',)

    def product_name(self, obj):
        return obj.product.title

    product_name.short_description = 'نام محصول'


# @admin.register(Spectaculation)
# class SpectaculationAdmin(admin.ModelAdmin):
#     form = AdminWYSIWYG


@admin.register(Favorite)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'liked_at',)
    list_filter = ('user',)
    search_fields = ('user','user__full_name',)



# admin.site.register(ProductImage)
admin.site.register(Speculation)
