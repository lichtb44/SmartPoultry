# SMARTPOULTRY - Poultry Farm Management System

A comprehensive, production-ready Django-based farm management system with machine learning capabilities for poultry operations. Features real-time analytics, financial tracking, production forecasting, and automated alerts.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![Django](https://img.shields.io/badge/django-4.2+-darkgreen)
![Database](https://img.shields.io/badge/database-PostgreSQL-blue)

## 🌟 Key Features

### Dashboard & Analytics
- Real-time KPI monitoring
- Revenue and expense tracking
- Production analytics
- Profit trend analysis
- Interactive Chart.js visualizations

### Flock Management
- Multi-flock tracking
- Breed information database
- Status monitoring
- Health and productivity records
- Production scheduling

### Production Records
- Daily production logs (eggs, meat, etc.)
- Mortality tracking with reasons
- Health & vaccination records
- Comprehensive breed information
- Historical data analysis

### Financial Management
- Revenue tracking (multiple product types)
- Expense categorization
- Cash flow analysis
- Monthly/Quarterly/Annual reports
- Financial projections

### Inventory System
- Real-time stock monitoring
- Automatic value calculations
- Feed and supply tracking
- Category-based organization
- Low stock alerts

### 🤖 Machine Learning
- **Profit Prediction** - 30-day forecast
- **Revenue Forecasting** - ML-based predictions
- **Production Forecasting** - Based on historical data
- **Anomaly Detection** - Alert on unusual patterns
- Models: RandomForest with Scikit-learn

### Notifications & Alerts
- High mortality warnings
- Low inventory alerts
- Production drop notifications
- Health issue alerts
- Expense surge warnings
- Customizable alert preferences

### User Management
- Role-based access control
- Multi-level permissions
- User profiles with farm info
- Activity tracking
- Custom role creation

### Reporting
- Daily/Weekly/Monthly/Annual reports
- Production analysis
- Financial summaries
- Data export capabilities
- Trend analysis

## 📋 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.9+, Django 4.2 |
| **API** | Django REST Framework |
| **Database** | PostgreSQL |
| **Frontend** | HTML5, CSS3, Bootstrap 5 |
| **Visualization** | Chart.js 3.7 |
| **ML/AI** | Pandas, NumPy, Scikit-learn |
| **Task Queue** | Joblib (ML models) |

## 🏗️ Project Structure

```
SMARTPOULTRY/
├── smartpoultry/                  # Django project root
│   ├── core/                      # Project settings & main URLs
│   ├── accounts/                  # User management & roles
│   ├── flocks/                    # Flock management
│   ├── production/                # Production & health records
│   ├── inventory/                 # Feed & supply inventory
│   ├── revenue/                   # Income tracking
│   ├── expenses/                  # Cost tracking
│   ├── analytics/                 # ML predictions
│   ├── reports/                   # Report generation
│   ├── notifications/             # Alerts & notifications
│   ├── static/                    # CSS, JS, images
│   └── templates/                 # HTML pages
├── ml_models/                     # ML model training & prediction
│   ├── train_model.py             # Model training script
│   ├── predictor.py               # Prediction utilities
│   └── README.md                  # ML documentation
├── manage.py                      # Django CLI
├── requirements.txt               # Python dependencies
├── .env                           # Environment variables
├── .env.example                   # Example env config
├── SETUP_GUIDE.md                 # Detailed setup guide
└── README.md                      # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- PostgreSQL 12+
- pip & virtualenv

### Installation

1. **Setup Environment**
```bash
cd SMARTPOULTRY
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure Database**
```bash
createdb smartpoultry
cp .env.example .env
# Edit .env with your database credentials
```

4. **Run Migrations**
```bash
cd smartpoultry
python manage.py migrate
```

5. **Create Admin User**
```bash
python manage.py createsuperuser
```

6. **Train ML Models** (Optional)
```bash
cd ../ml_models
python train_model.py
```

7. **Start Server**
```bash
cd ../smartpoultry
python manage.py runserver
```

Access at http://localhost:8000/

## 📡 API Documentation

### Base URL
```
http://localhost:8000/api/
```

### Main Endpoints
- `accounts/` - User management & roles
- `flocks/` - Flock management
- `production/` - Production & health records
- `inventory/` - Stock tracking
- `revenue/` - Income records
- `expenses/` - Cost tracking
- `analytics/` - Predictions
- `reports/` - Report generation
- `notifications/` - Alerts & notifications

[See SETUP_GUIDE.md for complete API documentation]

## 🤖 Machine Learning Features

### Training Models
```bash
cd ml_models
python train_model.py
```

### Using Predictions
```python
from predictor import get_predictor

predictor = get_predictor()
profit_forecast = predictor.forecast_profit_next_30_days(
    recent_revenue=[...],
    recent_expenses=[...]
)
```

### Supported Models
- RandomForest Profit Predictor
- RandomForest Revenue Forecaster
- Extensible for custom models

## 📊 Dashboard Features

- **KPI Cards**: Active flocks, total birds, monthly metrics
- **Revenue Chart**: Trend analysis with Chart.js
- **Expense Breakdown**: Pie chart visualization
- **Profit Analysis**: Performance tracking
- **Real-time Updates**: Live data synchronization

## 🔐 Security

- ✅ Role-based access control
- ✅ User authentication
- ✅ CSRF protection
- ✅ CORS configuration
- ✅ SQL injection prevention
- ✅ XSS protection
- ✅ Environment-based secrets

## 📚 Documentation

- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Complete setup & deployment guide
- [ml_models/README.md](ml_models/README.md) - ML model documentation
- [Django Docs](https://docs.djangoproject.com/)
- [DRF Docs](https://www.django-rest-framework.org/)

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test accounts

# With coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## 🚀 Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### Using Docker
```bash
docker build -t smartpoultry:latest .
docker run -d -p 8000:8000 smartpoultry:latest
```

[See SETUP_GUIDE.md for production configuration]

## 📋 Requirements

**Core Framework**
- Django 4.2.13
- djangorestframework 3.14.0
- psycopg2-binary 2.9.9

**Machine Learning**
- pandas 2.0.3
- numpy 1.24.3
- scikit-learn 1.3.0
- joblib 1.3.1

**Frontend** (CDN)
- Bootstrap 5.1.3
- Chart.js 3.7.1

[See requirements.txt for complete list]

## 🐛 Troubleshooting

### Database Issues
```bash
# Check connection
psql -U postgres -d smartpoultry

# Recreate database
dropdb smartpoultry
createdb smartpoultry
python manage.py migrate
```

### Migration Errors
```bash
python manage.py showmigrations
python manage.py migrate app_name zero
```

### Static Files
```bash
python manage.py collectstatic --clear --noinput
```

## 📝 Database Models

**Core Models**
- Farm, UserProfile, UserRole

**Production**
- Flock, ProductionRecord, MortalityRecord, HealthRecord, BreedInformation

**Financial**
- Revenue, Expense, Inventory

**Notifications**
- Notification, Alert, NotificationPreference

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/YourFeature`
3. Commit changes: `git commit -m 'Add YourFeature'`
4. Push branch: `git push origin feature/YourFeature`
5. Open Pull Request

## 📄 License

MIT License - See [LICENSE](LICENSE) for details

## 🗺️ Roadmap

**v1.1.0**
- [ ] Mobile app (React Native)
- [ ] Advanced ML (LSTM/Prophet)
- [ ] WebSocket notifications
- [ ] PDF/Excel export

**v1.2.0**
- [ ] IoT integration
- [ ] SMS alerts
- [ ] Multi-farm support
- [ ] Custom reports

**v1.3.0**
- [ ] Audit logging
- [ ] Auto backups
- [ ] Rate limiting
- [ ] Advanced analytics

## 💬 Support

- **Issues**: [GitHub Issues](../../issues)
- **Email**: support@smartpoultry.com
- **Docs**: [SETUP_GUIDE.md](SETUP_GUIDE.md)

## 👨‍💻 Team

SMARTPOULTRY Development Team

---

**Made with ❤️ for poultry farmers worldwide**

**v1.0.0** | [Changelog](CHANGELOG.md) | [License](LICENSE)
