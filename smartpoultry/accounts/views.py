from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile, UserRole
from .serializers import UserProfileSerializer, UserRoleSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for user management."""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]


class UserRoleViewSet(viewsets.ModelViewSet):
    """ViewSet for user roles."""
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [IsAuthenticated]
