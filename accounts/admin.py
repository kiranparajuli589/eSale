from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import User, Log, UserProfile


class MyUserAdmin(UserAdmin):
    list_display = ('upper_case_name', 'email', 'date_created', 'is_admin', 'is_staff', 'is_active')
    list_filter = ('is_admin', 'email')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('f_name', 'l_name')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_active')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )

    search_fields = ('email', 'f_name')
    date_hierarchy = 'date_created'
    ordering = ('f_name','date_created')

    filter_horizontal = ()


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'phone')
    list_filter = ('address',)
    search_fields = ('user__email', 'user__f_name', 'user__l_name', 'address')
    ordering = ('user',)


class LogAdmin(admin.ModelAdmin):
    list_display = ('date', 'user', 'subject', 'detail')
    search_fields = ('user', 'date')
    list_filter = ('user', 'date', 'subject')
    date_hierarchy = 'date'
    ordering = ('-date', 'user')


admin.site.register(User, MyUserAdmin)
admin.site.register(UserProfile, ProfileAdmin)
admin.site.register(Log, LogAdmin)
admin.site.unregister(Group)