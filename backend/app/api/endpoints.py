from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime
from pydantic import BaseModel

from app.database import get_db
from app.models import Product, Transaction
from app.schemas import ProductResponse
import sys
import os

# Add parent directory to path so we can import the ml module
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from ml.predict import predict_demand

router = APIRouter()

class PredictionRequest(BaseModel):
    stock_code: str
    unit_price: float
    target_date: datetime

class PredictionResponse(BaseModel):
    stock_code: str
    unit_price: float
    target_date: datetime
    predicted_quantity: float
    predicted_revenue: float

@router.get("/products", response_model=List[ProductResponse])
def get_products(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """
    Retrieve a paginated list of available products.
    """
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

@router.get("/analytics/summary")
def get_analytics_summary(db: Session = Depends(get_db)):
    """
    Retrieve high-level KPIs for the dashboard.
    """
    total_transactions = db.query(func.count(Transaction.id)).scalar()
    total_products = db.query(func.count(Product.StockCode)).scalar()
    
    # Calculate total revenue: Sum(Quantity * UnitPrice)
    # We join transactions and products to calculate this
    revenue_result = db.query(
        func.sum(Transaction.Quantity * Product.UnitPrice)
    ).join(Product, Transaction.StockCode == Product.StockCode).scalar()
    
    return {
        "total_transactions": total_transactions or 0,
        "total_unique_products": total_products or 0,
        "total_revenue": round(revenue_result or 0, 2)
    }

@router.post("/demand/predict", response_model=PredictionResponse)
def predict_product_demand(request: PredictionRequest, db: Session = Depends(get_db)):
    """
    Predict demand quantity for a product given a hypothetical price and date.
    Includes basic business logic guardrails.
    """
    if request.unit_price <= 0:
        raise HTTPException(status_code=400, detail="Unit price must be greater than 0.")
        
    # Verify product exists
    product = db.query(Product).filter(Product.StockCode == request.stock_code).first()
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with StockCode {request.stock_code} not found.")

    try:
        predicted_qty = predict_demand(
            stock_code=request.stock_code,
            unit_price=request.unit_price,
            target_date=request.target_date
        )
        
        return PredictionResponse(
            stock_code=request.stock_code,
            unit_price=request.unit_price,
            target_date=request.target_date,
            predicted_quantity=round(predicted_qty, 2),
            predicted_revenue=round(predicted_qty * request.unit_price, 2)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
