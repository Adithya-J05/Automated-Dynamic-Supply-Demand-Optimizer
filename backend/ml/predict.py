import os
import joblib
import pandas as pd
from datetime import datetime

ARTIFACTS_DIR = os.path.join(os.path.dirname(__file__), "artifacts")
MODEL_PATH = os.path.join(ARTIFACTS_DIR, "demand_model.joblib")

# Global singleton to hold the model in memory across API requests
_model_artifact = None

def load_model():
    """Load the model artifact into memory if not already loaded."""
    global _model_artifact
    if _model_artifact is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model artifact not found at {MODEL_PATH}. Please run train.py first.")
        _model_artifact = joblib.load(MODEL_PATH)
    return _model_artifact

def predict_demand(stock_code: str, unit_price: float, target_date: datetime) -> float:
    """
    Predicts the daily demand (Quantity) for a given product, price, and date.
    
    Args:
        stock_code: Product ID
        unit_price: Proposed Price
        target_date: The date for which demand is being predicted
    Returns:
        Predicted Quantity (float)
    """
    artifact = load_model()
    model = artifact['model']
    item_mean_sales = artifact['item_mean_sales']
    features = artifact['features']
    
    # Feature Engineering for the requested inference
    # Default to global mean if stock_code is new (Cold Start)
    global_mean = sum(item_mean_sales.values()) / len(item_mean_sales) if item_mean_sales else 0
    item_mean = item_mean_sales.get(stock_code, global_mean)
    
    day_of_week = target_date.weekday()
    month = target_date.month
    is_weekend = 1 if day_of_week >= 5 else 0
    
    # Construct the input dataframe matching the trained feature columns
    input_data = pd.DataFrame([{
        'UnitPrice': unit_price,
        'ItemMeanSales': item_mean,
        'DayOfWeek': day_of_week,
        'Month': month,
        'IsWeekend': is_weekend
    }], columns=features)
    
    prediction = model.predict(input_data)[0]
    
    # Ensure prediction is logically non-negative
    return max(0.0, float(prediction))

if __name__ == "__main__":
    # Simple manual verification
    print("Testing inference...")
    test_date = datetime.now()
    pred_qty = predict_demand(stock_code="85123A", unit_price=2.95, target_date=test_date)
    print(f"Predicted Demand for 85123A at $2.95 on {test_date.date()}: {pred_qty:.2f} units")
