from django.contrib import admin
from .models import Revenue


@admin.register(Revenue)
class RevenueAdmin(admin.ModelAdmin):
    list_display = ('revenue_type', 'quantity', 'unit', 'price_per_unit', 'total_amount', 'date')
    list_filter = ('revenue_type', 'date')
    search_fields = ('revenue_type',)
