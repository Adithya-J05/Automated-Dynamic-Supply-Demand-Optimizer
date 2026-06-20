from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List

# --- Product Schemas ---

class ProductBase(BaseModel):
    Description: Optional[str] = None
    UnitPrice: float

class ProductCreate(ProductBase):
    StockCode: str

class ProductResponse(ProductBase):
    StockCode: str
    
    model_config = ConfigDict(from_attributes=True)


# --- Transaction Schemas ---

class TransactionBase(BaseModel):
    InvoiceNo: str
    StockCode: str
    Quantity: int
    InvoiceDate: datetime
    CustomerID: float

class TransactionCreate(TransactionBase):
    DayOfWeek: int
    Month: int
    IsWeekend: int

class TransactionResponse(TransactionCreate):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
