from django.db import models
from flocks.models import Flock


class ProductionRecord(models.Model):
    """Daily production records for flocks."""
    PRODUCT_TYPES = [
        ('eggs', 'Eggs'),
        ('meat_ready', 'Meat Ready'),
        ('feathers', 'Feathers'),
        ('other', 'Other'),
    ]
    
    flock = models.ForeignKey(Flock, on_delete=models.CASCADE, related_name='production_records')
    product_type = models.CharField(max_length=50, choices=PRODUCT_TYPES)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50, default='units')
    date = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.flock} - {self.product_type} ({self.date})"
    
    class Meta:
        ordering = ['-date']
        unique_together = ('flock', 'product_type', 'date')


class MortalityRecord(models.Model):
    """Mortality records for flocks."""
    MORTALITY_REASONS = [
        ('disease', 'Disease'),
        ('predation', 'Predation'),
        ('stress', 'Stress'),
        ('accident', 'Accident'),
        ('age', 'Age'),
        ('unknown', 'Unknown'),
    ]
    
    flock = models.ForeignKey(Flock, on_delete=models.CASCADE, related_name='mortality_records')
    quantity = models.IntegerField()
    reason = models.CharField(max_length=50, choices=MORTALITY_REASONS, default='unknown')
    date = models.DateField()
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.flock} - {self.quantity} birds ({self.date})"
    
    class Meta:
        ordering = ['-date']


class BreedInformation(models.Model):
    """Detailed breed information."""
    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=50)
    egg_production_per_year = models.IntegerField(null=True, blank=True)
    growth_period_days = models.IntegerField(null=True, blank=True)
    average_weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feed_consumption_daily_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    lifespan_years = models.IntegerField(null=True, blank=True)
    characteristics = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Breed Information"


class HealthRecord(models.Model):
    """Health and vaccination records."""
    HEALTH_STATUS = [
        ('healthy', 'Healthy'),
        ('sick', 'Sick'),
        ('treated', 'Treated'),
        ('recovered', 'Recovered'),
    ]
    
    flock = models.ForeignKey(Flock, on_delete=models.CASCADE, related_name='health_records')
    health_status = models.CharField(max_length=50, choices=HEALTH_STATUS, default='healthy')
    disease_name = models.CharField(max_length=100, blank=True)
    treatment = models.TextField(blank=True)
    medication = models.CharField(max_length=255, blank=True)
    vaccination_name = models.CharField(max_length=100, blank=True)
    date = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.flock} - {self.health_status} ({self.date})"
    
    class Meta:
        ordering = ['-date']
