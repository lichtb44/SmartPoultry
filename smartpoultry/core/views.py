from datetime import timedelta

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db.models import Count, Q, Sum
from django.db.models.functions import TruncMonth
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.utils.text import capfirst
from .forms import MortalityRecordForm, ProductionRecordForm
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


def forgot_password(request):
    """Public password reset page for users who forgot their password."""
    if request.user.is_authenticated:
        if is_admin_user(request.user):
            return redirect('admin_dashboard')
        return redirect('dashboard')

    error = None
    success = None
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not email or not new_password or not confirm_password:
            error = 'Please fill out all fields.'
        elif new_password != confirm_password:
            error = 'Passwords do not match.'
        else:
            try:
                user = User.objects.get(email__iexact=email)
                validate_password(new_password, user)
            except User.DoesNotExist:
                error = 'No account was found with that email address.'
            except ValidationError as exc:
                error = ' '.join(exc.messages)
            else:
                user.set_password(new_password)
                user.save()
                success = 'Password reset successfully. You can now log in with your new password.'

    return render(request, 'forgot_password.html', {'error': error, 'success': success})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    """Dashboard view with overview."""
    if is_admin_user(request.user):
        return redirect('admin_dashboard')

    from expenses.models import Expense
    from flocks.models import Flock
    from inventory.models import Inventory
    from production.models import MortalityRecord, ProductionRecord
    from revenue.models import Revenue

    today = timezone.localdate()
    current_month_start = today.replace(day=1)
    if current_month_start.month == 1:
        previous_month_start = current_month_start.replace(year=current_month_start.year - 1, month=12)
    else:
        previous_month_start = current_month_start.replace(month=current_month_start.month - 1)

    def decimal_sum(queryset, field):
        return queryset.aggregate(total=Sum(field))['total'] or 0

    def percent_change(current, previous):
        if not previous:
            return None
        return round(((current - previous) / previous) * 100, 1)

    current_revenue = decimal_sum(Revenue.objects.filter(date__gte=current_month_start), 'total_amount')
    previous_revenue = decimal_sum(
        Revenue.objects.filter(date__gte=previous_month_start, date__lt=current_month_start),
        'total_amount',
    )
    current_expenses = decimal_sum(Expense.objects.filter(date__gte=current_month_start), 'amount')
    previous_expenses = decimal_sum(
        Expense.objects.filter(date__gte=previous_month_start, date__lt=current_month_start),
        'amount',
    )
    current_profit = current_revenue - current_expenses
    previous_profit = previous_revenue - previous_expenses
    feed_cost = decimal_sum(
        Expense.objects.filter(date__gte=current_month_start, expense_type='feed'),
        'amount',
    )
    production_total = decimal_sum(
        ProductionRecord.objects.filter(date__gte=current_month_start, product_type='eggs'),
        'quantity',
    )
    mortality_total = MortalityRecord.objects.filter(date__gte=current_month_start).aggregate(
        total=Sum('quantity')
    )['total'] or 0
    total_birds = Flock.objects.filter(status='active').aggregate(total=Sum('quantity'))['total'] or 0
    active_flocks = Flock.objects.filter(status='active').count()
    mortality_rate = round((mortality_total / total_birds) * 100, 2) if total_birds else 0
    feed_stock = decimal_sum(Inventory.objects.filter(item_type='feed'), 'quantity')
    feed_expense_share = round((feed_cost / current_expenses) * 100, 1) if current_expenses else 0

    trend_start = current_month_start
    for _ in range(5):
        if trend_start.month == 1:
            trend_start = trend_start.replace(year=trend_start.year - 1, month=12)
        else:
            trend_start = trend_start.replace(month=trend_start.month - 1)

    def month_key(value):
        return value.date() if hasattr(value, 'date') else value

    revenue_by_month = {
        month_key(item['month']): item['total'] or 0
        for item in Revenue.objects.filter(date__gte=trend_start)
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Sum('total_amount'))
    }
    expenses_by_month = {
        month_key(item['month']): item['total'] or 0
        for item in Expense.objects.filter(date__gte=trend_start)
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Sum('amount'))
    }
    feed_by_month = {
        month_key(item['month']): item['total'] or 0
        for item in Expense.objects.filter(date__gte=trend_start, expense_type='feed')
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Sum('amount'))
    }

    chart_months = []
    month_cursor = trend_start
    for _ in range(6):
        chart_months.append(month_cursor)
        if month_cursor.month == 12:
            month_cursor = month_cursor.replace(year=month_cursor.year + 1, month=1)
        else:
            month_cursor = month_cursor.replace(month=month_cursor.month + 1)

    revenue_values = [float(revenue_by_month.get(month, 0)) for month in chart_months]
    expense_values = [float(expenses_by_month.get(month, 0)) for month in chart_months]
    feed_values = [float(feed_by_month.get(month, 0)) for month in chart_months]
    profit_values = [revenue_values[index] - expense_values[index] for index in range(len(chart_months))]

    latest_notification = 'No recent notifications'
    try:
        from notifications.models import Notification
        notification = Notification.objects.filter(user=request.user).first()
        if notification:
            latest_notification = notification.title
    except Exception:
        pass

    context = {
        'date_range_label': f'{current_month_start:%b} 1 - {today:%b} {today.day}, {today.year}',
        'metrics': {
            'revenue': current_revenue,
            'revenue_change': percent_change(current_revenue, previous_revenue),
            'expenses': current_expenses,
            'expenses_change': percent_change(current_expenses, previous_expenses),
            'profit': current_profit,
            'profit_change': percent_change(current_profit, previous_profit),
            'cash_flow': current_profit,
            'feed_cost': feed_cost,
            'feed_expense_share': feed_expense_share,
            'mortality_rate': mortality_rate,
            'total_birds': total_birds,
            'active_flocks': active_flocks,
            'production_total': production_total,
            'feed_stock': feed_stock,
            'latest_notification': latest_notification,
        },
        'chart_data': {
            'labels': [capfirst(month.strftime('%b')) for month in chart_months],
            'revenue': revenue_values,
            'expenses': expense_values,
            'profit': profit_values,
            'feed': feed_values,
        },
    }
    return render(request, 'dashboard.html', context)


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
        'new_users_today': User.objects.filter(date_joined__date=timezone.localdate()).count(),
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
def admin_feedback_detail(request, feedback_id):
    """Read one feedback item and respond to it."""
    feedback = get_object_or_404(Feedback.objects.select_related('user'), pk=feedback_id)
    if request.method == 'POST':
        feedback.status = request.POST.get('status', feedback.status)
        feedback.admin_response = request.POST.get('admin_response', '').strip()
        feedback.save()
        messages.success(request, 'Feedback response saved.')
        return redirect('admin_feedback_detail', feedback_id=feedback.id)

    return render(request, 'admin_feedback_detail.html', {
        'feedback': feedback,
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
    from analytics.models import Prediction
    from expenses.models import Expense
    from production.models import ProductionRecord
    from revenue.models import Revenue

    today = timezone.localdate()
    current_month_start = today.replace(day=1)

    def add_months(value, months):
        month_index = value.month - 1 + months
        year = value.year + month_index // 12
        month = month_index % 12 + 1
        return value.replace(year=year, month=month, day=1)

    def decimal_sum(queryset, field):
        return queryset.aggregate(total=Sum(field))['total'] or 0

    def month_key(value):
        return value.date() if hasattr(value, 'date') else value

    def trend_forecast(values, periods):
        numeric_values = [float(value or 0) for value in values]
        if not numeric_values:
            return [0 for _ in range(periods)]
        if len(numeric_values) == 1:
            return [round(numeric_values[0], 2) for _ in range(periods)]

        recent_window = numeric_values[-3:] if len(numeric_values) >= 3 else numeric_values
        baseline = sum(recent_window) / len(recent_window)
        slope = (numeric_values[-1] - numeric_values[0]) / max(len(numeric_values) - 1, 1)
        return [round(max(0, baseline + slope * step), 2) for step in range(1, periods + 1)]

    history_start = add_months(current_month_start, -5)
    future_months = [add_months(current_month_start, offset) for offset in range(1, 7)]
    history_months = [add_months(history_start, offset) for offset in range(6)]

    revenue_by_month = {
        month_key(item['month']): item['total'] or 0
        for item in Revenue.objects.filter(date__gte=history_start)
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Sum('total_amount'))
    }
    expense_by_month = {
        month_key(item['month']): item['total'] or 0
        for item in Expense.objects.filter(date__gte=history_start)
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Sum('amount'))
    }

    actual_revenue = [float(revenue_by_month.get(month, 0)) for month in history_months]
    actual_expenses = [float(expense_by_month.get(month, 0)) for month in history_months]
    actual_profit = [
        round(actual_revenue[index] - actual_expenses[index], 2)
        for index in range(len(history_months))
    ]

    predicted_revenue = trend_forecast(actual_revenue, 6)
    predicted_expenses = trend_forecast(actual_expenses, 6)
    predicted_profit = [
        round(predicted_revenue[index] - predicted_expenses[index], 2)
        for index in range(len(future_months))
    ]

    week_starts = [today - timedelta(days=today.weekday() + (5 - index) * 7) for index in range(6)]
    production_by_week = []
    for week_start in week_starts:
        week_end = week_start + timedelta(days=7)
        production_by_week.append(float(decimal_sum(
            ProductionRecord.objects.filter(
                product_type='eggs',
                date__gte=week_start,
                date__lt=week_end,
            ),
            'quantity',
        )))
    predicted_production = trend_forecast(production_by_week, 6)

    method = 'SQLite recent trend forecast'
    for index, forecast_month in enumerate(future_months):
        Prediction.objects.update_or_create(
            prediction_type='profit',
            forecast_date=forecast_month,
            defaults={
                'predicted_value': predicted_profit[index],
                'method': method,
                'accuracy_percentage': 0,
            },
        )
        Prediction.objects.update_or_create(
            prediction_type='eggs',
            forecast_date=forecast_month,
            defaults={
                'predicted_value': predicted_production[index],
                'method': method,
                'accuracy_percentage': 0,
            },
        )

    latest_predictions = Prediction.objects.filter(
        prediction_type__in=['profit', 'eggs'],
        forecast_date__in=future_months,
    ).order_by('forecast_date', 'prediction_type')

    all_months = history_months + future_months
    chart_data = {
        'actualVsPredicted': {
            'labels': [capfirst(month.strftime('%b %Y')) for month in all_months],
            'actualRevenue': actual_revenue + [None for _ in future_months],
            'predictedRevenue': [None for _ in history_months] + predicted_revenue,
        },
        'profit': {
            'labels': [capfirst(month.strftime('%b %Y')) for month in future_months],
            'values': predicted_profit,
        },
        'production': {
            'labels': [f'Week {index}' for index in range(1, 7)],
            'actual': production_by_week,
            'predicted': predicted_production,
        },
    }

    return render(request, 'analytics.html', {
        'chart_data': chart_data,
        'latest_predictions': latest_predictions,
        'prediction_method': method,
        'last_updated': timezone.now(),
    })


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
def production_record_create(request):
    """Create a production record."""
    form = ProductionRecordForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Production record added.')
        return redirect('production_records')
    return render(request, 'production_record_form.html', {
        'form': form,
        'title': 'Add Production Record',
        'submit_label': 'Save Record',
    })


@login_required(login_url='login')
def production_record_update(request, record_id):
    """Edit a production record."""
    from production.models import ProductionRecord
    record = get_object_or_404(ProductionRecord, pk=record_id)
    form = ProductionRecordForm(request.POST or None, instance=record)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Production record updated.')
        return redirect('production_records')
    return render(request, 'production_record_form.html', {
        'form': form,
        'title': 'Edit Production Record',
        'submit_label': 'Update Record',
    })


@login_required(login_url='login')
def production_record_delete(request, record_id):
    """Delete a production record."""
    from production.models import ProductionRecord
    record = get_object_or_404(ProductionRecord, pk=record_id)
    if request.method == 'POST':
        record.delete()
        messages.success(request, 'Production record deleted.')
    return redirect('production_records')


@login_required(login_url='login')
def mortality_records_view(request):
    """Mortality records page."""
    from production.models import MortalityRecord
    records = MortalityRecord.objects.select_related('flock')[:50]
    return render(request, 'mortality_records.html', {'records': records})


@login_required(login_url='login')
def mortality_record_create(request):
    """Create a mortality record."""
    form = MortalityRecordForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Mortality record added.')
        return redirect('mortality_records')
    return render(request, 'mortality_record_form.html', {
        'form': form,
        'title': 'Add Mortality Record',
        'submit_label': 'Save Record',
    })


@login_required(login_url='login')
def mortality_record_update(request, record_id):
    """Edit a mortality record."""
    from production.models import MortalityRecord
    record = get_object_or_404(MortalityRecord, pk=record_id)
    form = MortalityRecordForm(request.POST or None, instance=record)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Mortality record updated.')
        return redirect('mortality_records')
    return render(request, 'mortality_record_form.html', {
        'form': form,
        'title': 'Edit Mortality Record',
        'submit_label': 'Update Record',
    })


@login_required(login_url='login')
def mortality_record_delete(request, record_id):
    """Delete a mortality record."""
    from production.models import MortalityRecord
    record = get_object_or_404(MortalityRecord, pk=record_id)
    if request.method == 'POST':
        record.delete()
        messages.success(request, 'Mortality record deleted.')
    return redirect('mortality_records')


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
