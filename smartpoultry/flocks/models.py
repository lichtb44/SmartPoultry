from django.db import models
from django.utils import timezone


class Flock(models.Model):
    """Flock/batch of poultry."""
    BREED_CHOICES = [
        ('layers', 'Layers'),
        ('broilers', 'Broilers'),
        ('ducks', 'Ducks'),
        ('turkeys', 'Turkeys'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('sold', 'Sold'),
        ('deceased', 'Deceased'),
        ('retired', 'Retired'),
    ]

    flock_id = models.CharField(max_length=100, unique=True)
    breed = models.CharField(max_length=50, choices=BREED_CHOICES)
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    date_added = models.DateField(auto_now_add=True)
    expected_production_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.flock_id} - {self.breed} ({self.quantity})"

    class Meta:
        ordering = ['-date_added']
