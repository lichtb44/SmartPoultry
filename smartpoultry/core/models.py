from django.db import models
from django.conf import settings


class Farm(models.Model):
    """Main farm information model."""
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_farm')
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    established_date = models.DateField()
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Farms"
