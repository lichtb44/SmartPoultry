from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ProductionRecordViewSet, MortalityRecordViewSet, 
                   BreedInformationViewSet, HealthRecordViewSet)

router = DefaultRouter()
router.register(r'records', ProductionRecordViewSet, basename='production')
router.register(r'mortality', MortalityRecordViewSet, basename='mortality')
router.register(r'breeds', BreedInformationViewSet, basename='breed')
router.register(r'health', HealthRecordViewSet, basename='health')

urlpatterns = [
    path('', include(router.urls)),
]
