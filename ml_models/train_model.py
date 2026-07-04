"""
Machine Learning Model Training for SMARTPOULTRY

This script trains predictive models for:
- Profit prediction
- Revenue forecasting
- Production forecasting
"""

import os
import sys
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
from datetime import datetime, timedelta

# Add Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

from django.db.models import Sum
from revenue.models import Revenue
from expenses.models import Expense
from analytics.models import Prediction


class PredictionModelTrainer:
    """Train and manage ML prediction models."""
    
    def __init__(self, model_dir='ml_models'):
        self.model_dir = model_dir
        self.profit_model = None
        self.revenue_model = None
        self.scaler = StandardScaler()
        os.makedirs(model_dir, exist_ok=True)
    
    def prepare_financial_data(self, months_back=12):
        """Prepare historical financial data for training."""
        print("📊 Preparing financial data...")
        
        # Get historical data
        cutoff_date = datetime.now() - timedelta(days=30*months_back)
        revenues = Revenue.objects.filter(date__gte=cutoff_date)
        expenses = Expense.objects.filter(date__gte=cutoff_date)
        
        # Create daily aggregates
        data = []
        current_date = cutoff_date.date()
        end_date = datetime.now().date()
        
        while current_date <= end_date:
            daily_revenue = revenues.filter(date=current_date).aggregate(
                total=Sum('total_amount')
            )['total'] or 0
            
            daily_expense = expenses.filter(date=current_date).aggregate(
                total=Sum('amount')
            )['total'] or 0
            
            profit = daily_revenue - daily_expense
            
            data.append({
                'date': current_date,
                'revenue': float(daily_revenue),
                'expenses': float(daily_expense),
                'profit': float(profit),
                'day_of_week': current_date.weekday(),
                'day_of_month': current_date.day,
                'month': current_date.month,
            })
            
            current_date += timedelta(days=1)
        
        return pd.DataFrame(data)
    
    def train_profit_model(self):
        """Train profit prediction model using RandomForest."""
        print("🤖 Training Profit Prediction Model...")
        
        # Prepare data
        df = self.prepare_financial_data(months_back=12)
        
        if len(df) < 30:
            print("⚠️  Insufficient data for training. Need at least 30 data points.")
            return False
        
        # Features and target
        features = ['day_of_week', 'day_of_month', 'month', 'revenue', 'expenses']
        X = df[features].values
        y = df['profit'].values
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.profit_model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        self.profit_model.fit(X_train_scaled, y_train)
        
        # Evaluate
        train_score = self.profit_model.score(X_train_scaled, y_train)
        test_score = self.profit_model.score(X_test_scaled, y_test)
        
        print(f"✅ Profit Model - Train R²: {train_score:.4f}, Test R²: {test_score:.4f}")
        
        # Save model
        model_path = os.path.join(self.model_dir, 'profit_prediction.pkl')
        joblib.dump(self.profit_model, model_path)
        scaler_path = os.path.join(self.model_dir, 'profit_scaler.pkl')
        joblib.dump(self.scaler, scaler_path)
        print(f"💾 Model saved to {model_path}")
        
        return True
    
    def train_revenue_model(self):
        """Train revenue forecasting model."""
        print("🤖 Training Revenue Forecast Model...")
        
        df = self.prepare_financial_data(months_back=12)
        
        if len(df) < 30:
            print("⚠️  Insufficient data for training.")
            return False
        
        features = ['day_of_week', 'day_of_month', 'month']
        X = df[features].values
        y = df['revenue'].values
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        self.revenue_model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        self.revenue_model.fit(X_train, y_train)
        
        train_score = self.revenue_model.score(X_train, y_train)
        test_score = self.revenue_model.score(X_test, y_test)
        
        print(f"✅ Revenue Model - Train R²: {train_score:.4f}, Test R²: {test_score:.4f}")
        
        model_path = os.path.join(self.model_dir, 'revenue_forecast.pkl')
        joblib.dump(self.revenue_model, model_path)
        print(f"💾 Model saved to {model_path}")
        
        return True
    
    def predict_profit(self, days_ahead=30):
        """Predict profit for future days."""
        print(f"📈 Predicting profit for next {days_ahead} days...")
        
        if not os.path.exists(os.path.join(self.model_dir, 'profit_prediction.pkl')):
            print("❌ Model not found. Train model first.")
            return None
        
        self.profit_model = joblib.load(
            os.path.join(self.model_dir, 'profit_prediction.pkl')
        )
        scaler_path = os.path.join(self.model_dir, 'profit_scaler.pkl')
        if os.path.exists(scaler_path):
            self.scaler = joblib.load(scaler_path)
        
        predictions = []
        current_date = datetime.now().date()
        
        for i in range(days_ahead):
            future_date = current_date + timedelta(days=i)
            
            # Simple features (can be enhanced)
            features = np.array([[
                future_date.weekday(),
                future_date.day,
                future_date.month,
                50000,  # Estimated revenue
                30000,  # Estimated expenses
            ]])
            
            features_scaled = self.scaler.transform(features)
            predicted_profit = self.profit_model.predict(features_scaled)[0]
            
            predictions.append({
                'date': future_date,
                'predicted_profit': max(0, predicted_profit),
            })
        
        return pd.DataFrame(predictions)


def train_all_models():
    """Train all prediction models."""
    print("\n🚀 SMARTPOULTRY ML Model Training\n")
    print("=" * 50)
    
    trainer = PredictionModelTrainer()
    
    # Train models
    trainer.train_profit_model()
    print()
    trainer.train_revenue_model()
    
    print("\n" + "=" * 50)
    print("✨ Model training completed!")
    print(f"📁 Models saved in: ml_models/")


if __name__ == '__main__':
    train_all_models()
