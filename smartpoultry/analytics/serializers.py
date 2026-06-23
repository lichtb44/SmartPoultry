from rest_framework import serializers
from .models import Prediction


class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = ['id', 'prediction_type', 'forecast_date', 'predicted_value', 
                  'actual_value', 'accuracy_percentage', 'method', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
