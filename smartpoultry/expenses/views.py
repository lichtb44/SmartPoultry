from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from notifications.utils import create_activity_notification
from .models import Expense
from .serializers import ExpenseSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    """ViewSet for managing expenses."""
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        expense = serializer.save()
        create_activity_notification(
            self.request.user,
            f"Successfully added {expense.get_expense_type_display().lower()} expense",
            f"Recorded expense of PHP {expense.amount} for {expense.description}.",
            expense,
        )
