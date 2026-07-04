from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from notifications.utils import create_activity_notification
from .models import Inventory, FeedType
from .serializers import InventorySerializer, FeedTypeSerializer


class InventoryViewSet(viewsets.ModelViewSet):
    """ViewSet for managing inventory."""
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Inventory.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        item = serializer.save(user=self.request.user)
        create_activity_notification(
            self.request.user,
            f"Successfully added {item.name} to feed and inventory",
            f"{item.quantity} {item.unit} of {item.get_item_type_display().lower()} inventory was added.",
            item,
        )


class FeedTypeViewSet(viewsets.ModelViewSet):
    """ViewSet for feed types."""
    queryset = FeedType.objects.all()
    serializer_class = FeedTypeSerializer
    permission_classes = [IsAuthenticated]
