from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Prediction
from .serializers import PredictionSerializer


class PredictionViewSet(viewsets.ModelViewSet):
    """ViewSet for predictions and analytics."""
    queryset = Prediction.objects.all()
    serializer_class = PredictionSerializer
    permission_classes = [IsAuthenticated]
