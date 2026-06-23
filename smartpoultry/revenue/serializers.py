from rest_framework import serializers
from .models import Revenue


class RevenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revenue
        fields = ['id', 'revenue_type', 'flock', 'quantity', 'unit', 'price_per_unit',
                  'total_amount', 'date', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'total_amount', 'created_at', 'updated_at']
