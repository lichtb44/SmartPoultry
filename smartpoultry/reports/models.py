from django.db import models
from django.conf import settings


class Report(models.Model):
    """Generated reports."""
    REPORT_TYPES = [
        ('daily', 'Daily Report'),
        ('weekly', 'Weekly Report'),
        ('monthly', 'Monthly Report'),
        ('quarterly', 'Quarterly Report'),
        ('annual', 'Annual Report'),
        ('production', 'Production Report'),
        ('financial', 'Financial Report'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports', null=True, blank=True)
    report_type = models.CharField(max_length=50, choices=REPORT_TYPES)
    title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    summary = models.TextField(blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.start_date} to {self.end_date})"

    class Meta:
        ordering = ['-generated_at']
