from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Revenue
from .serializers import RevenueSerializer


class RevenueViewSet(viewsets.ModelViewSet):
    """ViewSet for managing revenue."""
    queryset = Revenue.objects.all()
    serializer_class = RevenueSerializer
    permission_classes = [IsAuthenticated]
