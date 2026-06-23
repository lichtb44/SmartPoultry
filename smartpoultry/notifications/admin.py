from django.contrib import admin
from .models import Notification, Alert, NotificationPreference


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'title', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('user__username', 'title', 'message')


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('alert_type', 'title', 'severity', 'status', 'farm', 'created_at')
    list_filter = ('alert_type', 'status', 'severity', 'created_at')
    search_fields = ('title', 'description')


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'email_alerts', 'email_notifications', 'in_app_notifications')
    list_filter = ('email_alerts', 'email_notifications', 'in_app_notifications')
