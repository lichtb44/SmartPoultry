from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Flock
from .serializers import FlockSerializer


class FlockViewSet(viewsets.ModelViewSet):
    """ViewSet for managing flocks."""
    queryset = Flock.objects.all()
    serializer_class = FlockSerializer
    permission_classes = [IsAuthenticated]
