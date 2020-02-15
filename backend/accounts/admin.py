from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, ResetPasswordCode, User, UserActivationCode


class MyUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'date_joined', 'is_superuser')
    list_filter = ('is_superuser', 'is_customer')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'gender')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active', 'is_vendor', 'is_customer')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
         ),
    )

    search_fields = ('email', 'username')
    date_hierarchy = 'date_joined'
    ordering = ('username', 'date_joined')

    filter_horizontal = ()


admin.site.register(UserProfile)
admin.site.register(ResetPasswordCode)
admin.site.register(UserActivationCode)
admin.site.register(User, MyUserAdmin)
