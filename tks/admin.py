from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User
# Register your models here.
class UserAdmin(UserAdmin):
    fieldsets = (
    (None, {
        'fields': ('username', 'password')
    }),
    ('Personal info', {
        'fields': ('first_name', 'last_name', 'email')
    }),
    ('Permissions', {
        'fields': (
            'is_active', 'is_staff', 'is_superuser',
            'groups', 'user_permissions'
            )
    }),
    ('Important dates', {
        'fields': ('last_login', 'date_joined')
    }),
    ('Additional info', {
        'fields': ('tupc_id', 'role', 'year_course', 'user_img', 'has_ongoing_transaction')
    })
)

admin.site.register(User, UserAdmin)