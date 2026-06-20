import os
import joblib
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

# Adjust imports to work if executed as a module or standalone script
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database import engine, SQLALCHEMY_DATABASE_URL

ARTIFACTS_DIR = os.path.join(os.path.dirname(__file__), "artifacts")
MODEL_PATH = os.path.join(ARTIFACTS_DIR, "demand_model.joblib")

def fetch_data():
    """Fetch raw transaction data from PostgreSQL."""
    print("Fetching data from PostgreSQL...")
    query = """
        SELECT t."StockCode", t."Quantity", t."InvoiceDate", p."UnitPrice", t."DayOfWeek", t."Month", t."IsWeekend"
        FROM transactions t
        JOIN products p ON t."StockCode" = p."StockCode"
    """
    df = pd.read_sql(query, SQLALCHEMY_DATABASE_URL)
    return df

def preprocess_data(df: pd.DataFrame):
    """Aggregate to daily level per product."""
    print("Preprocessing data...")
    # Truncate InvoiceDate to just the Date
    df['Date'] = pd.to_datetime(df['InvoiceDate']).dt.date
    
    # Group by StockCode and Date to get daily aggregate demand
    # We take the sum of Quantity, and average of UnitPrice, DayOfWeek, Month, IsWeekend
    daily_df = df.groupby(['StockCode', 'Date']).agg({
        'Quantity': 'sum',
        'UnitPrice': 'mean',
        'DayOfWeek': 'first',
        'Month': 'first',
        'IsWeekend': 'first'
    }).reset_index()
    
    # Remove extreme outliers (returns or massive wholesale anomalies)
    # Keeping items where daily quantity is between 0 and 99th percentile
    q99 = daily_df['Quantity'].quantile(0.99)
    daily_df = daily_df[(daily_df['Quantity'] > 0) & (daily_df['Quantity'] <= q99)]
    
    return daily_df

def train_model():
    """Train the Demand Forecasting Random Forest."""
    df = fetch_data()
    if df.empty:
        print("No data found in the database. Run data_loader.py first.")
        return

    df = preprocess_data(df)
    
    # Feature Engineering
    # We will use StockCode frequency (target encoding proxy) to help the model distinguish items
    # For a production system, proper target encoding or embeddings is preferred
    item_mean_sales = df.groupby('StockCode')['Quantity'].mean().to_dict()
    df['ItemMeanSales'] = df['StockCode'].map(item_mean_sales)
    
    # Features (X) and Target (y)
    features = ['UnitPrice', 'ItemMeanSales', 'DayOfWeek', 'Month', 'IsWeekend']
    X = df[features]
    y = df['Quantity']
    
    print(f"Training on {len(X)} daily product records...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    
    # Evaluate
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    
    print(f"Model Evaluation -> MAE: {mae:.2f}, R2: {r2:.2f}")
    
    # Save the model and the item mean sales lookup dictionary together
    artifact = {
        'model': model,
        'item_mean_sales': item_mean_sales,
        'features': features
    }
    
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    joblib.dump(artifact, MODEL_PATH)
    print(f"Model successfully saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_model()
