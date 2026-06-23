from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Expense
from .serializers import ExpenseSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    """ViewSet for managing expenses."""
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
