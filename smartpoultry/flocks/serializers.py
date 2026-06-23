from rest_framework import serializers
from .models import Flock


class FlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flock
        fields = ['id', 'flock_id', 'breed', 'quantity', 'status', 'date_added', 
                  'expected_production_date', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
