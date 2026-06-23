from rest_framework import serializers
from .models import ProductionRecord, MortalityRecord, BreedInformation, HealthRecord


class ProductionRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionRecord
        fields = ['id', 'flock', 'product_type', 'quantity', 'unit', 'date', 'notes', 'created_at']
        read_only_fields = ['id', 'created_at']


class MortalityRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MortalityRecord
        fields = ['id', 'flock', 'quantity', 'reason', 'date', 'description', 'notes', 'created_at']
        read_only_fields = ['id', 'created_at']


class BreedInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BreedInformation
        fields = ['id', 'name', 'type', 'egg_production_per_year', 'growth_period_days', 
                  'average_weight_kg', 'feed_consumption_daily_kg', 'lifespan_years', 'characteristics']
        read_only_fields = ['id']


class HealthRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthRecord
        fields = ['id', 'flock', 'health_status', 'disease_name', 'treatment', 'medication', 
                  'vaccination_name', 'date', 'notes', 'created_at']
        read_only_fields = ['id', 'created_at']
