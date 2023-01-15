from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, RpiIP
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

class RpiIPAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

admin.site.register(User, UserAdmin)
admin.site.register(RpiIP, RpiIPAdmin)