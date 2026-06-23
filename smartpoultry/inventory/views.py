from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Inventory, FeedType
from .serializers import InventorySerializer, FeedTypeSerializer


class InventoryViewSet(viewsets.ModelViewSet):
    """ViewSet for managing inventory."""
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated]


class FeedTypeViewSet(viewsets.ModelViewSet):
    """ViewSet for feed types."""
    queryset = FeedType.objects.all()
    serializer_class = FeedTypeSerializer
    permission_classes = [IsAuthenticated]
