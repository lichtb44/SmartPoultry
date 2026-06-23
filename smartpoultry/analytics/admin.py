from django.contrib import admin
from .models import Prediction


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('prediction_type', 'forecast_date', 'predicted_value', 'actual_value', 'accuracy_percentage')
    list_filter = ('prediction_type', 'forecast_date')
