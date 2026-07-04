from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Report
from .serializers import ReportSerializer


class ReportViewSet(viewsets.ModelViewSet):
    """ViewSet for managing reports."""
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Report.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
