from django.contrib import admin
from .models import Inventory, FeedType


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'item_type', 'quantity', 'unit', 'total_value', 'last_updated')
    list_filter = ('item_type', 'last_updated')
    search_fields = ('name',)


@admin.register(FeedType)
class FeedTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit', 'cost_per_unit')
