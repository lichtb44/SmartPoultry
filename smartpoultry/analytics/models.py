from django.db import models
from django.utils import timezone


class Prediction(models.Model):
    """Production predictions and forecasts."""
    PREDICTION_TYPES = [
        ('eggs', 'Egg Production'),
        ('meat', 'Meat Production'),
        ('profit', 'Profit Forecast'),
        ('expenses', 'Expense Forecast'),
    ]

    prediction_type = models.CharField(max_length=50, choices=PREDICTION_TYPES)
    forecast_date = models.DateField()
    predicted_value = models.DecimalField(max_digits=15, decimal_places=2)
    actual_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    accuracy_percentage = models.FloatField(default=0)
    method = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.prediction_type} - {self.forecast_date}"

    class Meta:
        ordering = ['-forecast_date']
