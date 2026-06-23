from django.db import models


class Expense(models.Model):
    """Expense/cost tracking."""
    EXPENSE_TYPES = [
        ('feed', 'Feed'),
        ('medicine', 'Medicine'),
        ('equipment', 'Equipment'),
        ('labor', 'Labor'),
        ('utilities', 'Utilities'),
        ('maintenance', 'Maintenance'),
        ('other', 'Other'),
    ]

    expense_type = models.CharField(max_length=50, choices=EXPENSE_TYPES)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField()
    category = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.expense_type.upper()} - {self.amount} ({self.date})"

    class Meta:
        ordering = ['-date']
