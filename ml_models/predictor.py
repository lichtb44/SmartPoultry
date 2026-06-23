"""
ML Models and Utilities for SMARTPOULTRY

This module provides machine learning predictions for:
- Profit forecasting
- Revenue prediction
- Production forecasting
- Anomaly detection
"""

import os
import joblib
import numpy as np
import pandas as pd
from django.utils import timezone
from datetime import timedelta


class MLPredictor:
    """Load and use trained ML models for predictions."""
    
    def __init__(self, model_dir='ml_models'):
        self.model_dir = model_dir
        self.profit_model = None
        self.revenue_model = None
        self.scaler = None
        self._load_models()
    
    def _load_models(self):
        """Load trained models from disk."""
        profit_path = os.path.join(self.model_dir, 'profit_prediction.pkl')
        revenue_path = os.path.join(self.model_dir, 'revenue_forecast.pkl')
        
        if os.path.exists(profit_path):
            self.profit_model = joblib.load(profit_path)
        
        if os.path.exists(revenue_path):
            self.revenue_model = joblib.load(revenue_path)
    
    def predict_profit(self, features):
        """Predict profit using trained model."""
        if not self.profit_model:
            return None
        return self.profit_model.predict([features])[0]
    
    def predict_revenue(self, features):
        """Predict revenue using trained model."""
        if not self.revenue_model:
            return None
        return self.revenue_model.predict([features])[0]
    
    def forecast_profit_next_30_days(self, recent_revenue, recent_expenses):
        """Forecast profit for next 30 days."""
        if not self.profit_model:
            return None
        
        predictions = []
        today = timezone.now().date()
        
        for i in range(30):
            future_date = today + timedelta(days=i)
            # Use average recent data for prediction
            avg_revenue = np.mean(recent_revenue) if recent_revenue else 50000
            avg_expenses = np.mean(recent_expenses) if recent_expenses else 30000
            
            features = [
                future_date.weekday(),
                future_date.day,
                future_date.month,
                avg_revenue,
                avg_expenses,
            ]
            
            try:
                predicted_profit = self.predict_profit(features)
                predictions.append({
                    'date': future_date,
                    'predicted_profit': max(0, predicted_profit),
                    'confidence': 0.85  # Can be improved with model confidence scores
                })
            except:
                pass
        
        return pd.DataFrame(predictions)


def get_predictor():
    """Factory function to get ML predictor instance."""
    return MLPredictor()
