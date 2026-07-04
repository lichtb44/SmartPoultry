from rest_framework import serializers
from .models import Revenue


class RevenueSerializer(serializers.ModelSerializer):
    def validate_flock(self, flock):
        request = self.context.get('request')
        if flock and request and flock.user_id != request.user.id:
            raise serializers.ValidationError('Select one of your own flocks.')
        return flock

    class Meta:
        model = Revenue
        fields = ['id', 'revenue_type', 'flock', 'quantity', 'unit', 'price_per_unit',
                  'total_amount', 'date', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'total_amount', 'created_at', 'updated_at']
