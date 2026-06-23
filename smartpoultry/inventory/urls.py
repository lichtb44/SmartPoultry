from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InventoryViewSet, FeedTypeViewSet

router = DefaultRouter()
router.register(r'items', InventoryViewSet, basename='inventory')
router.register(r'feed-types', FeedTypeViewSet, basename='feed_type')

urlpatterns = [
    path('', include(router.urls)),
]
