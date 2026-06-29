from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()


def index(request):
    """Login page view."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    error = None
    if request.method == 'POST':
        identifier = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        if identifier and password:
            username = identifier
            if '@' in identifier:
                try:
                    user_obj = User.objects.get(email__iexact=identifier)
                    username = user_obj.username
                except User.DoesNotExist:
                    username = identifier
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return redirect('dashboard')
            error = 'Invalid login credentials. Please try again.'
        else:
            error = 'Email and password are required.'
    return render(request, 'index.html', {'error': error})


def register(request):
    """User registration page view."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        if not username or not email or not password or not password2:
            error = 'Please fill out all fields.'
        elif password != password2:
            error = 'Passwords do not match.'
        elif User.objects.filter(username=username).exists():
            error = 'Username already taken.'
        elif User.objects.filter(email=email).exists():
            error = 'Email already registered.'
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('dashboard')
    return render(request, 'register.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('index')


@login_required(login_url='login')
def dashboard(request):
    """Dashboard view with overview."""
    return render(request, 'dashboard.html')


@login_required(login_url='login')
def flocks(request):
    """Flocks management view."""
    return render(request, 'flocks.html')


@login_required(login_url='login')
def inventory_view(request):
    """Inventory management view."""
    return render(request, 'inventory.html')


@login_required(login_url='login')
def revenue_view(request):
    """Revenue tracking view."""
    return render(request, 'revenue.html')


@login_required(login_url='login')
def expenses_view(request):
    """Expenses tracking view."""
    return render(request, 'expenses.html')


@login_required(login_url='login')
def analytics_view(request):
    """Analytics and predictions view."""
    return render(request, 'analytics.html')


@login_required(login_url='login')
def reports_view(request):
    """Reports view."""
    return render(request, 'reports.html')
