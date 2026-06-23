from django.db import models
from flocks.models import Flock


class Revenue(models.Model):
    """Revenue/income tracking."""
    REVENUE_TYPES = [
        ('eggs', 'Eggs'),
        ('meat', 'Meat'),
        ('birds', 'Birds'),
        ('manure', 'Manure'),
        ('other', 'Other'),
    ]

    revenue_type = models.CharField(max_length=50, choices=REVENUE_TYPES)
    flock = models.ForeignKey(Flock, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50, default='units')
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, editable=False)
    date = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.total_amount = self.quantity * self.price_per_unit
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.revenue_type.upper()} - {self.total_amount} ({self.date})"

    class Meta:
        ordering = ['-date']
