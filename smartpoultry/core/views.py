from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db.models import Count, Q
from django.http import HttpResponseForbidden
from .models import Feedback

User = get_user_model()


def is_admin_user(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def admin_required(view_func):
    """Allow access only to staff or superuser accounts."""
    @login_required(login_url='login')
    def wrapper(request, *args, **kwargs):
        if is_admin_user(request.user):
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden('You do not have permission to access this page.')
    return wrapper


def index(request):
    """Login page view."""
    if request.user.is_authenticated:
        if is_admin_user(request.user):
            return redirect('admin_dashboard')
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
                if is_admin_user(user):
                    return redirect('admin_dashboard')
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
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    """Dashboard view with overview."""
    if is_admin_user(request.user):
        return redirect('admin_dashboard')
    return render(request, 'dashboard.html')


@login_required(login_url='login')
def profile_view(request):
    """Manage the signed-in user's profile."""
    if request.method == 'POST':
        user = request.user
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()

        if not username or not email:
            messages.error(request, 'Username and email are required.')
        elif User.objects.exclude(pk=user.pk).filter(username=username).exists():
            messages.error(request, 'That username is already taken.')
        elif User.objects.exclude(pk=user.pk).filter(email=email).exists():
            messages.error(request, 'That email is already registered.')
        else:
            user.username = username
            user.email = email
            user.first_name = request.POST.get('first_name', '').strip()
            user.last_name = request.POST.get('last_name', '').strip()
            user.phone = request.POST.get('phone', '').strip()
            user.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')

    return render(request, 'profile.html')


@login_required(login_url='login')
def settings_view(request):
    """Account settings for password and notification preferences."""
    preference = None
    try:
        from notifications.models import NotificationPreference
        preference, _ = NotificationPreference.objects.get_or_create(user=request.user)
    except Exception:
        preference = None

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'notifications' and preference:
            preference.email_alerts = request.POST.get('email_alerts') == 'on'
            preference.email_notifications = request.POST.get('email_notifications') == 'on'
            preference.in_app_notifications = request.POST.get('in_app_notifications') == 'on'
            preference.push_notifications = request.POST.get('push_notifications') == 'on'
            preference.save()
            messages.success(request, 'Notification settings updated.')
            return redirect('settings')

        if action == 'password':
            current_password = request.POST.get('current_password', '')
            new_password = request.POST.get('new_password', '')
            confirm_password = request.POST.get('confirm_password', '')

            if not request.user.check_password(current_password):
                messages.error(request, 'Current password is incorrect.')
            elif new_password != confirm_password:
                messages.error(request, 'New passwords do not match.')
            else:
                try:
                    validate_password(new_password, request.user)
                except ValidationError as exc:
                    messages.error(request, ' '.join(exc.messages))
                else:
                    request.user.set_password(new_password)
                    request.user.save()
                    update_session_auth_hash(request, request.user)
                    messages.success(request, 'Password updated successfully.')
                    return redirect('settings')

    return render(request, 'settings.html', {'preference': preference})


@login_required(login_url='login')
def feedback_view(request):
    """Allow users to submit feedback or reviews."""
    if request.method == 'POST':
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        rating = request.POST.get('rating', '5')

        if not subject or not message:
            messages.error(request, 'Subject and message are required.')
        else:
            try:
                rating = max(1, min(5, int(rating)))
            except ValueError:
                rating = 5
            Feedback.objects.create(
                user=request.user,
                subject=subject,
                message=message,
                rating=rating,
            )
            messages.success(request, 'Thank you. Your feedback was submitted.')
            return redirect('feedback')

    feedback_items = Feedback.objects.filter(user=request.user)
    return render(request, 'feedback.html', {'feedback_items': feedback_items})


@admin_required
def admin_dashboard(request):
    """Admin dashboard for user accounts and feedback management."""
    query = request.GET.get('q', '').strip()
    users = User.objects.select_related('farm').order_by('username')
    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )

    feedback_items = Feedback.objects.select_related('user').all()[:10]
    stats = {
        'total_users': User.objects.count(),
        'active_users': User.objects.filter(is_active=True, is_active_user=True).count(),
        'inactive_users': User.objects.filter(Q(is_active=False) | Q(is_active_user=False)).count(),
        'new_feedback': Feedback.objects.filter(status='new').count(),
    }
    feedback_status_counts = Feedback.objects.values('status').annotate(total=Count('id'))

    return render(request, 'admin_dashboard.html', {
        'managed_users': users,
        'feedback_items': feedback_items,
        'feedback_status_counts': feedback_status_counts,
        'stats': stats,
        'query': query,
    })


@admin_required
def admin_toggle_user(request, user_id):
    if request.method != 'POST':
        return redirect('admin_dashboard')

    target_user = get_object_or_404(User, pk=user_id)
    if target_user.pk == request.user.pk:
        messages.error(request, 'You cannot deactivate your own account.')
    else:
        activate = request.POST.get('action') == 'activate'
        target_user.is_active = activate
        target_user.is_active_user = activate
        target_user.save()
        messages.success(request, f"{target_user.username} has been {'activated' if activate else 'deactivated'}.")
    return redirect('admin_dashboard')


@admin_required
def admin_delete_user(request, user_id):
    if request.method != 'POST':
        return redirect('admin_dashboard')

    target_user = get_object_or_404(User, pk=user_id)
    if target_user.pk == request.user.pk:
        messages.error(request, 'You cannot delete your own account.')
    elif target_user.is_superuser and not request.user.is_superuser:
        messages.error(request, 'Only a superuser can delete another superuser.')
    else:
        username = target_user.username
        target_user.delete()
        messages.success(request, f'{username} was deleted.')
    return redirect('admin_dashboard')


@admin_required
def admin_reset_user_password(request, user_id):
    target_user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        else:
            try:
                validate_password(new_password, target_user)
            except ValidationError as exc:
                messages.error(request, ' '.join(exc.messages))
            else:
                target_user.set_password(new_password)
                target_user.save()
                messages.success(request, f'Password reset for {target_user.username}.')
                return redirect('admin_dashboard')

    return render(request, 'admin_reset_password.html', {'target_user': target_user})


@admin_required
def admin_feedback(request):
    feedback_items = Feedback.objects.select_related('user').all()
    status = request.GET.get('status', '').strip()
    if status:
        feedback_items = feedback_items.filter(status=status)
    return render(request, 'admin_feedback.html', {
        'feedback_items': feedback_items,
        'status': status,
        'status_choices': Feedback.STATUS_CHOICES,
    })


@admin_required
def admin_update_feedback(request, feedback_id):
    if request.method != 'POST':
        return redirect('admin_feedback')

    feedback = get_object_or_404(Feedback, pk=feedback_id)
    feedback.status = request.POST.get('status', feedback.status)
    feedback.admin_response = request.POST.get('admin_response', '').strip()
    feedback.save()
    messages.success(request, 'Feedback updated.')
    return redirect('admin_feedback')


@admin_required
def admin_delete_feedback(request, feedback_id):
    if request.method == 'POST':
        feedback = get_object_or_404(Feedback, pk=feedback_id)
        feedback.delete()
        messages.success(request, 'Feedback deleted.')
    return redirect('admin_feedback')


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


@login_required(login_url='login')
def production_records_view(request):
    """Production records page."""
    from production.models import ProductionRecord
    records = ProductionRecord.objects.select_related('flock')[:50]
    return render(request, 'production_records.html', {'records': records})


@login_required(login_url='login')
def mortality_records_view(request):
    """Mortality records page."""
    from production.models import MortalityRecord
    records = MortalityRecord.objects.select_related('flock')[:50]
    return render(request, 'mortality_records.html', {'records': records})


@login_required(login_url='login')
def forecasting_view(request):
    """Forecasting page."""
    return render(request, 'forecasting.html')


@login_required(login_url='login')
def scenario_analysis_view(request):
    """Scenario analysis page."""
    return render(request, 'scenario_analysis.html')


@login_required(login_url='login')
def notifications_page(request):
    """User notifications page."""
    from notifications.models import Notification
    notifications = Notification.objects.filter(user=request.user)[:50]
    return render(request, 'notifications_page.html', {'notifications': notifications})
