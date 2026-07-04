from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from notifications.utils import create_activity_notification
from .models import ProductionRecord, MortalityRecord, BreedInformation, HealthRecord
from .serializers import (ProductionRecordSerializer, MortalityRecordSerializer,
                         BreedInformationSerializer, HealthRecordSerializer)


class ProductionRecordViewSet(viewsets.ModelViewSet):
    """ViewSet for production records."""
    queryset = ProductionRecord.objects.all()
    serializer_class = ProductionRecordSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        record = serializer.save()
        create_activity_notification(
            self.request.user,
            f"Successfully added {record.get_product_type_display().lower()} production record",
            f"Recorded {record.quantity} {record.unit} for flock {record.flock.flock_id} on {record.date}.",
            record,
        )


class MortalityRecordViewSet(viewsets.ModelViewSet):
    """ViewSet for mortality records."""
    queryset = MortalityRecord.objects.all()
    serializer_class = MortalityRecordSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        record = serializer.save()
        record.flock.refresh_from_db()
        create_activity_notification(
            self.request.user,
            "Successfully added mortality record",
            (
                f"Recorded {record.quantity} mortality for flock {record.flock.flock_id} due to "
                f"{record.get_reason_display().lower()}. Remaining flock quantity: {record.flock.quantity}."
            ),
            record,
        )


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
