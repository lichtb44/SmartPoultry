from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from notifications.utils import create_activity_notification
from .models import Revenue
from .serializers import RevenueSerializer


class RevenueViewSet(viewsets.ModelViewSet):
    """ViewSet for managing revenue."""
    serializer_class = RevenueSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Revenue.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        revenue = serializer.save(user=self.request.user)
        create_activity_notification(
            self.request.user,
            f"Successfully added {revenue.get_revenue_type_display().lower()} revenue",
            f"Recorded revenue of PHP {revenue.total_amount} from {revenue.quantity} {revenue.unit}.",
            revenue,
        )
