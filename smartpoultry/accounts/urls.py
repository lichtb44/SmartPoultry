from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, UserRoleViewSet

router = DefaultRouter()
router.register(r'users', UserProfileViewSet, basename='user')
router.register(r'roles', UserRoleViewSet, basename='role')

urlpatterns = [
    path('', include(router.urls)),
]
