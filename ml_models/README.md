# ML Models Placeholder

This directory contains machine learning models for SMARTPOULTRY predictions.

## Models

- **profit_prediction.pkl** - RandomForest model for profit forecasting
- **revenue_forecast.pkl** - RandomForest model for revenue prediction

## Training

To train the models:

```bash
cd ml_models
python train_model.py
```

## Usage

```python
from predictor import get_predictor

predictor = get_predictor()
profit_prediction = predictor.predict_profit([...features...])
```

## Files

- `train_model.py` - Model training script
- `predictor.py` - Prediction utilities
