from rest_framework import serializers
from .models import ProductionRecord, MortalityRecord, BreedInformation, HealthRecord


class ProductionRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionRecord
        fields = ['id', 'flock', 'product_type', 'quantity', 'unit', 'date', 'notes', 'created_at']
        read_only_fields = ['id', 'created_at']


class MortalityRecordSerializer(serializers.ModelSerializer):
    flock_id_display = serializers.CharField(source='flock.flock_id', read_only=True)

    class Meta:
        model = MortalityRecord
        fields = [
            'id',
            'flock',
            'flock_id_display',
            'quantity',
            'reason',
            'date',
            'description',
            'notes',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def validate(self, attrs):
        flock = attrs.get('flock', getattr(self.instance, 'flock', None))
        quantity = attrs.get('quantity', getattr(self.instance, 'quantity', None))
        if flock is None or quantity is None:
            return attrs

        if quantity <= 0:
            raise serializers.ValidationError({'quantity': 'Mortality quantity must be greater than zero.'})

        available_quantity = flock.quantity
        if self.instance and self.instance.flock_quantity_applied and self.instance.flock_id == flock.id:
            available_quantity += self.instance.quantity

        if quantity > available_quantity:
            raise serializers.ValidationError({
                'quantity': f'Mortality quantity cannot exceed the selected flock quantity ({available_quantity}).'
            })
        return attrs


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
