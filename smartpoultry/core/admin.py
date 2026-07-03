from django.contrib import admin
from .models import Farm, Feedback, TransactionRecord


@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'location', 'contact_email', 'created_at')
    search_fields = ('name', 'owner__username', 'location', 'contact_email')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'rating', 'status', 'created_at')
    list_filter = ('status', 'rating', 'created_at')
    search_fields = ('subject', 'message', 'user__username', 'user__email')


@admin.register(TransactionRecord)
class TransactionRecordAdmin(admin.ModelAdmin):
    list_display = (
        'transaction_type',
        'action',
        'amount',
        'description',
        'transaction_date',
        'source_label',
        'created_at',
    )
    list_filter = ('transaction_type', 'action', 'transaction_date', 'created_at')
    search_fields = ('description', 'source_label', 'notes')
    readonly_fields = (
        'transaction_type',
        'action',
        'amount',
        'description',
        'transaction_date',
        'source_content_type',
        'source_object_id',
        'source_label',
        'notes',
        'metadata',
        'created_at',
    )
