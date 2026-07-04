from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Prediction
from .serializers import PredictionSerializer


class PredictionViewSet(viewsets.ModelViewSet):
    """ViewSet for predictions and analytics."""
    serializer_class = PredictionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Prediction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
