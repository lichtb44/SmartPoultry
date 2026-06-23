# SMARTPOULTRY Quick Reference

## 🚀 Common Commands

### Setup & Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create database
createdb smartpoultry

# Copy environment config
cp .env.example .env
```

### Django Management

```bash
cd smartpoultry

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run development server
python manage.py runserver

# Run specific port
python manage.py runserver 8001

# Create new app
python manage.py startapp app_name

# Drop database
python manage.py sqlflush | psql

# Check migrations
python manage.py showmigrations

# Test project
python manage.py test

# Test specific app
python manage.py test accounts
```

### Machine Learning

```bash
cd ml_models

# Train all models
python train_model.py

# Check if models exist
ls *.pkl

cd ../smartpoultry
```

### Database

```bash
# PostgreSQL console
psql -U postgres -d smartpoultry

# Create database
createdb smartpoultry

# Drop database
dropdb smartpoultry

# Backup database
pg_dump smartpoultry > backup.sql

# Restore database
psql smartpoultry < backup.sql
```

### Useful Django Queries

```python
python manage.py shell

# Import models
from flocks.models import Flock
from accounts.models import UserProfile
from revenue.models import Revenue

# Query examples
flock = Flock.objects.first()
flocks = Flock.objects.filter(status='active')
revenue = Revenue.objects.aggregate(total=Sum('total_amount'))
users = UserProfile.objects.filter(role='admin')

# Create objects
flock = Flock.objects.create(
    flock_id='F001',
    breed='layers',
    quantity=100,
    status='active'
)

# Update objects
flock.quantity = 150
flock.save()

# Delete objects
flock.delete()
```

## 📡 API Endpoints

### Test API Calls

```bash
# List flocks
curl http://localhost:8000/api/flocks/

# List inventory
curl http://localhost:8000/api/inventory/items/

# List revenue
curl http://localhost:8000/api/revenue/

# List expenses
curl http://localhost:8000/api/expenses/

# List users
curl http://localhost:8000/api/accounts/users/

# List alerts
curl http://localhost:8000/api/notifications/alerts/
```

### Using Python Requests

```python
import requests

# Get all flocks
response = requests.get('http://localhost:8000/api/flocks/')
flocks = response.json()

# Create flock
data = {
    'flock_id': 'F002',
    'breed': 'broilers',
    'quantity': 500,
    'status': 'active'
}
response = requests.post('http://localhost:8000/api/flocks/', json=data)

# Get prediction
response = requests.get('http://localhost:8000/api/analytics/')
predictions = response.json()
```

## 🔍 Debugging

### Check Logs

```bash
# Django development logs (in terminal)
python manage.py runserver

# Database connection
python manage.py dbshell

# Check static files
python manage.py findstatic css/style.css
```

### Python Debugging

```bash
# Use Python shell
python manage.py shell

# Interactive debugging
import pdb; pdb.set_trace()

# Pretty print
from pprint import pprint
pprint(object)
```

## 📁 File Locations

```
Configuration Files:
├── smartpoultry/core/settings.py      # Django settings
├── smartpoultry/core/urls.py          # Main URLs
├── .env                               # Environment variables
└── requirements.txt                   # Dependencies

Django Apps:
├── smartpoultry/accounts/             # User management
├── smartpoultry/flocks/               # Flock management
├── smartpoultry/production/           # Production records
├── smartpoultry/inventory/            # Inventory
├── smartpoultry/revenue/              # Revenue
├── smartpoultry/expenses/             # Expenses
├── smartpoultry/analytics/            # Analytics
├── smartpoultry/reports/              # Reports
└── smartpoultry/notifications/        # Notifications

Frontend:
├── smartpoultry/templates/            # HTML pages
├── smartpoultry/static/css/           # Stylesheets
└── smartpoultry/static/js/            # JavaScript

ML:
└── ml_models/                         # ML models
```

## 🐛 Common Issues & Solutions

### Database Connection Error
```bash
# Check PostgreSQL is running
sudo service postgresql status

# Check credentials in .env
cat .env | grep DB_

# Test connection
psql -U postgres -d smartpoultry
```

### Migration Issues
```bash
# Show all migrations
python manage.py showmigrations

# Undo migrations
python manage.py migrate app_name zero

# Create new migrations
python manage.py makemigrations
```

### Static Files Not Loading
```bash
python manage.py collectstatic --clear --noinput
python manage.py findstatic css/style.css
```

### Port Already in Use
```bash
# Use different port
python manage.py runserver 8001

# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

### ML Model Not Found
```bash
cd ml_models
python train_model.py
# Wait for training to complete
ls *.pkl  # Verify files exist
```

## 📊 Database Models Quick Reference

### Accounts
```python
from accounts.models import UserProfile, UserRole

UserProfile: username, email, role, phone, farm, is_active_user
UserRole: name, permissions, description, is_custom
```

### Flocks
```python
from flocks.models import Flock

Flock: flock_id, breed, quantity, status, date_added, expected_production_date
```

### Production
```python
from production.models import ProductionRecord, MortalityRecord, HealthRecord, BreedInformation

ProductionRecord: flock, product_type, quantity, unit, date
MortalityRecord: flock, quantity, reason, date, description
HealthRecord: flock, health_status, disease_name, treatment, vaccination_name, date
BreedInformation: name, type, egg_production_per_year, growth_period_days
```

### Financial
```python
from revenue.models import Revenue
from expenses.models import Expense
from inventory.models import Inventory

Revenue: revenue_type, flock, quantity, unit, price_per_unit, date
Expense: expense_type, description, amount, date, category
Inventory: item_type, name, quantity, unit, cost_per_unit
```

## 🎯 Useful Django Shell Commands

```bash
python manage.py shell

# Get object count
from flocks.models import Flock
Flock.objects.count()

# Get all flocks
flocks = Flock.objects.all()
for flock in flocks:
    print(flock.flock_id, flock.quantity)

# Get summary statistics
from django.db.models import Sum, Avg
Flock.objects.aggregate(total=Sum('quantity'), avg=Avg('quantity'))

# Filter by date
from datetime import datetime, timedelta
last_month = datetime.now() - timedelta(days=30)
recent_revenue = Revenue.objects.filter(date__gte=last_month)

# Get user with specific role
from accounts.models import UserProfile
admins = UserProfile.objects.filter(role='admin')

# Delete old records
from datetime import datetime, timedelta
old_date = datetime.now() - timedelta(days=365)
ProductionRecord.objects.filter(date__lt=old_date).delete()
```

## 📚 Useful Links

- Django Docs: https://docs.djangoproject.com/
- DRF Docs: https://www.django-rest-framework.org/
- PostgreSQL: https://www.postgresql.org/docs/
- Scikit-learn: https://scikit-learn.org/
- Bootstrap: https://getbootstrap.com/
- Chart.js: https://www.chartjs.org/

## 🚀 Deployment Checklist

```bash
# Before deploying
[ ] Update SECRET_KEY in .env
[ ] Set DEBUG=False
[ ] Configure ALLOWED_HOSTS
[ ] Test with DEBUG=False locally
[ ] Collect static files
[ ] Run migrations on production database
[ ] Create backup
[ ] Set up SSL certificate
[ ] Configure email settings
[ ] Set up monitoring/logging
```

## 💡 Pro Tips

1. **Use Django shell for quick testing**
   ```bash
   python manage.py shell_plus  # Requires django-extensions
   ```

2. **Database browser**
   ```bash
   pgAdmin for PostgreSQL GUI
   ```

3. **API testing**
   ```bash
   Postman or Insomnia for API testing
   ```

4. **Real-time monitoring**
   ```bash
   python manage.py runserver --pdb
   ```

5. **Faster migrations**
   ```bash
   python manage.py migrate --parallel
   ```

---

**Happy Coding! 🎉**
