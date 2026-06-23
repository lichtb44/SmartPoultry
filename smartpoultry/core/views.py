from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def index(request):
    """Home page view."""
    return render(request, 'index.html')


@login_required(login_url='admin:login')
def dashboard(request):
    """Dashboard view with overview."""
    return render(request, 'dashboard.html')


@login_required(login_url='admin:login')
def flocks(request):
    """Flocks management view."""
    return render(request, 'flocks.html')


@login_required(login_url='admin:login')
def inventory_view(request):
    """Inventory management view."""
    return render(request, 'inventory.html')


@login_required(login_url='admin:login')
def revenue_view(request):
    """Revenue tracking view."""
    return render(request, 'revenue.html')


@login_required(login_url='admin:login')
def expenses_view(request):
    """Expenses tracking view."""
    return render(request, 'expenses.html')


@login_required(login_url='admin:login')
def analytics_view(request):
    """Analytics and predictions view."""
    return render(request, 'analytics.html')


@login_required(login_url='admin:login')
def reports_view(request):
    """Reports view."""
    return render(request, 'reports.html')
