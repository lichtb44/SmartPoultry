"""
URL configuration for SMARTPOULTRY project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.index, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/flocks/', include('flocks.urls')),
    path('api/inventory/', include('inventory.urls')),
    path('api/revenue/', include('revenue.urls')),
    path('api/expenses/', include('expenses.urls')),
    path('api/analytics/', include('analytics.urls')),
    path('api/reports/', include('reports.urls')),
    path('api/production/', include('production.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('flocks/', views.flocks, name='flocks'),
    path('inventory/', views.inventory_view, name='inventory'),
    path('revenue/', views.revenue_view, name='revenue'),
    path('expenses/', views.expenses_view, name='expenses'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('reports/', views.reports_view, name='reports'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
