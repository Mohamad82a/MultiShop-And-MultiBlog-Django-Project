from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm

from account.models import User, Otp
from .models import Address


class AddressInline(admin.StackedInline):
    model = Address
    extra = 0
    classes = ['collapse']

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    # add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["phone",'full_name',"is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["phone", "password"]}),
        ("اطلاعات شخصی", {"fields": ["full_name", 'melicode', "email"]}),
        ("دسترسی ها", {"fields": ["is_admin"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email","phone" , "full_name" ,"password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []
    inlines = [AddressInline]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    search_fields = ['full_name','phone','user__melicode', 'user__full_name']


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
admin.site.register(Otp)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)