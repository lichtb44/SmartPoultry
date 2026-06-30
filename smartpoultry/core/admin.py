from django.contrib import admin
from .models import Farm, Feedback


@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'location', 'contact_email', 'created_at')
    search_fields = ('name', 'owner__username', 'location', 'contact_email')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'rating', 'status', 'created_at')
    list_filter = ('status', 'rating', 'created_at')
    search_fields = ('subject', 'message', 'user__username', 'user__email')
