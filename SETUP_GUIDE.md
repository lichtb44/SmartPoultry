# SMARTPOULTRY Complete Setup Guide

## Project Overview

SMARTPOULTRY is a comprehensive poultry farm management system featuring:
- Django REST API backend
- PostgreSQL database
- Machine Learning predictions
- Responsive Bootstrap frontend
- Real-time analytics with Chart.js

## System Architecture

```
SMARTPOULTRY/
├── smartpoultry/              # Django project
│   ├── core/                  # Settings & main URLs
│   ├── accounts/              # User management & roles
│   ├── flocks/                # Flock management
│   ├── production/            # Production & health records
│   ├── inventory/             # Inventory tracking
│   ├── revenue/               # Revenue tracking
│   ├── expenses/              # Expense tracking
│   ├── analytics/             # Predictions
│   ├── reports/               # Reporting
│   ├── notifications/         # Alerts & notifications
│   ├── static/                # CSS, JS, images
│   └── templates/             # HTML templates
├── ml_models/                 # ML models & training
│   ├── train_model.py         # Training script
│   └── predictor.py           # Prediction utilities
├── manage.py                  # Django management
├── requirements.txt           # Dependencies
└── .env                       # Environment config
```

## Prerequisites

- Python 3.9+
- PostgreSQL 12+
- pip & virtualenv
- Git

## Installation Steps

### 1. Clone & Setup

```bash
cd SMARTPOULTRY
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. PostgreSQL Setup

```bash
# Create database
createdb smartpoultry

# Create user (optional)
createuser smartpoultry_user
```

### 4. Environment Configuration

Create/update `.env`:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=smartpoultry
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# ML Models
ML_MODEL_DIR=ml_models
```

### 5. Run Migrations

```bash
cd smartpoultry
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Admin User

```bash
python manage.py createsuperuser
```

### 7. Train ML Models (Optional)

```bash
cd ../ml_models
python train_model.py
```

### 8. Collect Static Files

```bash
cd ../smartpoultry
python manage.py collectstatic --noinput
```

### 9. Run Development Server

```bash
python manage.py runserver
```

Access:
- Frontend: http://localhost:8000/
- Admin: http://localhost:8000/admin/
- API: http://localhost:8000/api/

## Key Features

### 1. Dashboard
- Real-time KPIs
- Revenue & expense tracking
- Production analytics
- Profit trends

### 2. Flock Management
- Add/edit/delete flocks
- Track breed information
- Monitor flock status
- Production scheduling

### 3. Production Records
- Daily production logs
- Mortality tracking
- Health records
- Breed information database

### 4. Financial Management
- Revenue tracking (eggs, meat, etc.)
- Expense categorization
- Cash flow analysis
- Financial reports

### 5. Inventory System
- Feed & supply tracking
- Stock level monitoring
- Automatic cost calculations
- Item categorization

### 6. Machine Learning
- Profit prediction (30-day forecast)
- Revenue forecasting
- Production forecasting
- Anomaly detection

### 7. Notifications
- Automated alerts
- Health warnings
- Expense notifications
- Low inventory alerts

### 8. Reporting
- Daily/Weekly/Monthly reports
- Financial summaries
- Production analysis
- Export capabilities

## API Endpoints

### Accounts
```
GET    /api/accounts/users/              # List users
POST   /api/accounts/users/              # Create user
GET    /api/accounts/users/{id}/         # Get user
PUT    /api/accounts/users/{id}/         # Update user
DELETE /api/accounts/users/{id}/         # Delete user

GET    /api/accounts/roles/              # List roles
```

### Flocks
```
GET    /api/flocks/                      # List flocks
POST   /api/flocks/                      # Create flock
GET    /api/flocks/{id}/                 # Get flock
PUT    /api/flocks/{id}/                 # Update flock
DELETE /api/flocks/{id}/                 # Delete flock
```

### Production
```
GET    /api/production/records/          # Production records
GET    /api/production/mortality/        # Mortality records
GET    /api/production/health/           # Health records
GET    /api/production/breeds/           # Breed info
```

### Financial
```
GET    /api/revenue/                     # Revenue records
GET    /api/expenses/                    # Expense records
GET    /api/inventory/items/             # Inventory
```

### Analytics & Reports
```
GET    /api/analytics/                   # Predictions
GET    /api/reports/                     # Reports
GET    /api/notifications/               # Notifications
GET    /api/notifications/alerts/        # Alerts
```

## Database Models

### Core Tables
- **Farm** - Farm information
- **UserProfile** - Users with roles
- **Flock** - Poultry flocks
- **BreedInformation** - Breed database

### Production
- **ProductionRecord** - Daily production logs
- **MortalityRecord** - Bird mortality tracking
- **HealthRecord** - Health & vaccination records

### Financial
- **Revenue** - Income records
- **Expense** - Expense records
- **Inventory** - Stock tracking

### Notifications
- **Notification** - User notifications
- **Alert** - Automated alerts
- **NotificationPreference** - User preferences

## Machine Learning

### Training Models

```bash
cd ml_models
python train_model.py
```

### Using Predictions

```python
from predictor import get_predictor

predictor = get_predictor()

# Predict profit
features = [weekday, day, month, revenue, expenses]
profit = predictor.predict_profit(features)

# Forecast next 30 days
forecast = predictor.forecast_profit_next_30_days(
    recent_revenue=[...],
    recent_expenses=[...]
)
```

## Development

### Creating New Features

```bash
# Create new Django app
python manage.py startapp feature_name

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### Running Tests

```bash
python manage.py test
```

### Code Style

- Follow PEP 8
- Use meaningful variable names
- Document complex functions
- Add docstrings to classes

## Deployment

### Using Gunicorn

```bash
pip install gunicorn
gunicorn core.wsgi:application --bind 0.0.0.0:8000
```

### Using Docker

```bash
docker build -t smartpoultry:latest .
docker run -d -p 8000:8000 smartpoultry:latest
```

### Environment Variables for Production

```env
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECRET_KEY=your-long-random-secret-key
DB_HOST=production-db-host
DB_PASSWORD=strong-password
```

## Security Checklist

- [ ] Change SECRET_KEY in production
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS/SSL
- [ ] Set up CORS properly
- [ ] Regular database backups
- [ ] Implement rate limiting
- [ ] Log security events
- [ ] Keep dependencies updated

## Troubleshooting

### Database Connection Error
```bash
# Check PostgreSQL is running
psql -U postgres -d smartpoultry

# Reset migrations
python manage.py migrate app_name zero
```

### Static Files Not Loading
```bash
python manage.py collectstatic --clear --noinput
```

### Permission Denied
```bash
# Check user roles
python manage.py createsuperuser
```

### ML Model Errors
```bash
# Retrain models
cd ml_models
python train_model.py
```

## Performance Tips

- Enable query result caching
- Use database indexing
- Implement pagination
- Optimize Chart.js rendering
- Use CDN for static files
- Enable gzip compression
- Implement lazy loading

## Support & Documentation

- Django Docs: https://docs.djangoproject.com/
- DRF: https://www.django-rest-framework.org/
- Scikit-learn: https://scikit-learn.org/
- Bootstrap: https://getbootstrap.com/
- Chart.js: https://www.chartjs.org/

## Roadmap

- [ ] Mobile app (React Native)
- [ ] Advanced ML models
- [ ] IoT device integration
- [ ] SMS alerts
- [ ] Multi-farm dashboard
- [ ] Custom reports builder
- [ ] Audit logs
- [ ] Data backup automation

## License

MIT License - See LICENSE file

## Contributors

SMARTPOULTRY Development Team

## Version

v1.0.0 - Complete Implementation
