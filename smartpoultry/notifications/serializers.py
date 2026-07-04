from rest_framework import serializers
from .models import Notification, Alert, NotificationPreference


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'notification_type', 'title', 'message', 'is_read', 
                  'created_at', 'read_at']
        read_only_fields = ['id', 'user', 'created_at']


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ['id', 'alert_type', 'status', 'title', 'description', 'severity',
                  'threshold_value', 'current_value', 'farm', 'created_at', 'acknowledged_at']
        read_only_fields = ['id', 'created_at']


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreference
        fields = ['id', 'user', 'email_alerts', 'email_notifications', 'in_app_notifications',
                  'push_notifications', 'quiet_hours_start', 'quiet_hours_end']
        read_only_fields = ['id', 'user']
