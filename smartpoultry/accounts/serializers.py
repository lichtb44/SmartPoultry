from rest_framework import serializers
from .models import UserProfile, UserRole


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ['id', 'name', 'description', 'is_custom']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone', 
                  'role', 'farm', 'is_active_user']
        read_only_fields = ['id']
