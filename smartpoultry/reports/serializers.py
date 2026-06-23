from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'report_type', 'title', 'start_date', 'end_date', 
                  'summary', 'generated_at', 'updated_at']
        read_only_fields = ['id', 'generated_at', 'updated_at']
