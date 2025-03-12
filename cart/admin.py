from django.contrib import admin
from .models import Order, OrderItem, DiscountCode, UserDiscountCode
from account.models import User, Address
# Register your models here.

class OrderItemStackInline(admin.StackedInline):
    model = OrderItem
    classes = ['collapse']
    extra = 0


@admin.register(Order)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user','total_price', 'item_quantities','get_user_full_name', 'is_paid','order_date',)
    inlines = [OrderItemStackInline]
    search_fields = ['user__username', 'user__melicode', 'user__phone']
    list_filter = ['is_paid']

    def get_user_full_name(self, request):
        return request.user.full_name
    get_user_full_name.short_description = 'نام کاربر'


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'quantity', 'discount')

# admin.site.register(OrderItem)
admin.site.register(UserDiscountCode)
