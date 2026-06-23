from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FlockViewSet

router = DefaultRouter()
router.register(r'', FlockViewSet, basename='flock')

urlpatterns = [
    path('', include(router.urls)),
]
