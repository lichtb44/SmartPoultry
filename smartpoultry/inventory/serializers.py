from rest_framework import serializers
from .models import Inventory, FeedType


class FeedTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedType
        fields = ['id', 'name', 'unit', 'cost_per_unit']


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['id', 'item_type', 'name', 'quantity', 'unit', 'cost_per_unit', 
                  'total_value', 'date_added', 'last_updated', 'notes']
        read_only_fields = ['id', 'total_value', 'date_added', 'last_updated']
