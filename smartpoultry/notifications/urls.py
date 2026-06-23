from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet, AlertViewSet, NotificationPreferenceViewSet

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'alerts', AlertViewSet, basename='alert')
router.register(r'preferences', NotificationPreferenceViewSet, basename='preference')

urlpatterns = [
    path('', include(router.urls)),
]
