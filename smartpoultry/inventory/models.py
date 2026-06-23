from django.db import models


class FeedType(models.Model):
    """Types of feed available."""
    name = models.CharField(max_length=100, unique=True)
    unit = models.CharField(max_length=50, default='kg')
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Inventory(models.Model):
    """Feed and supply inventory tracking."""
    ITEM_TYPES = [
        ('feed', 'Feed'),
        ('medicine', 'Medicine'),
        ('equipment', 'Equipment'),
        ('other', 'Other'),
    ]

    item_type = models.CharField(max_length=50, choices=ITEM_TYPES)
    name = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50)
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_value = models.DecimalField(max_digits=15, decimal_places=2, editable=False)
    date_added = models.DateField(auto_now_add=True)
    last_updated = models.DateField(auto_now=True)
    notes = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        self.total_value = self.quantity * self.cost_per_unit
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"

    class Meta:
        ordering = ['-last_updated']
