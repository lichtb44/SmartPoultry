from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Notification, Alert, NotificationPreference
from .serializers import NotificationSerializer, AlertSerializer, NotificationPreferenceSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    """ViewSet for notifications."""
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def mark_as_read(self, request):
        """Mark all notifications as read."""
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({'status': 'notifications marked as read'})
    
    @action(detail=True, methods=['post'])
    def read(self, request, pk=None):
        """Mark specific notification as read."""
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'notification marked as read'})


class AlertViewSet(viewsets.ModelViewSet):
    """ViewSet for alerts."""
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        """Acknowledge an alert."""
        alert = self.get_object()
        alert.status = 'acknowledged'
        alert.save()
        return Response({'status': 'alert acknowledged'})
    
    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """Resolve an alert."""
        alert = self.get_object()
        alert.status = 'resolved'
        alert.save()
        return Response({'status': 'alert resolved'})


class NotificationPreferenceViewSet(viewsets.ModelViewSet):
    """ViewSet for notification preferences."""
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return NotificationPreference.objects.filter(user=self.request.user)
