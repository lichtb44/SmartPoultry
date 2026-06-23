from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import ProductionRecord, MortalityRecord, BreedInformation, HealthRecord
from .serializers import (ProductionRecordSerializer, MortalityRecordSerializer,
                         BreedInformationSerializer, HealthRecordSerializer)


class ProductionRecordViewSet(viewsets.ModelViewSet):
    """ViewSet for production records."""
    queryset = ProductionRecord.objects.all()
    serializer_class = ProductionRecordSerializer
    permission_classes = [IsAuthenticated]


class MortalityRecordViewSet(viewsets.ModelViewSet):
    """ViewSet for mortality records."""
    queryset = MortalityRecord.objects.all()
    serializer_class = MortalityRecordSerializer
    permission_classes = [IsAuthenticated]


class BreedInformationViewSet(viewsets.ModelViewSet):
    """ViewSet for breed information."""
    queryset = BreedInformation.objects.all()
    serializer_class = BreedInformationSerializer
    permission_classes = [IsAuthenticated]


class HealthRecordViewSet(viewsets.ModelViewSet):
    """ViewSet for health records."""
    queryset = HealthRecord.objects.all()
    serializer_class = HealthRecordSerializer
    permission_classes = [IsAuthenticated]
