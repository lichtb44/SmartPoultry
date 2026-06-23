from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile, UserRole


@admin.register(UserProfile)
class UserProfileAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'farm', 'is_active_user')
    list_filter = ('role', 'is_active_user', 'created_at')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Farm Info', {'fields': ('phone', 'role', 'farm', 'is_active_user')}),
    )


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_custom', 'created_at')
    list_filter = ('is_custom', 'created_at')
