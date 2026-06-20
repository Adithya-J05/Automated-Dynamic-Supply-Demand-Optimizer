from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Product(Base):
    __tablename__ = "products"

    StockCode = Column(String, primary_key=True, index=True)
    Description = Column(String)
    UnitPrice = Column(Float)

    # Relationship to transactions
    transactions = relationship("Transaction", back_populates="product")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True) # Surrogate primary key
    InvoiceNo = Column(String, index=True)
    StockCode = Column(String, ForeignKey("products.StockCode"), index=True)
    Quantity = Column(Integer)
    InvoiceDate = Column(DateTime, index=True)
    CustomerID = Column(Float, index=True) # Float because pandas often reads missing IDs as NaN, we'll clean to int but keep DB flexible or change to String if alphanumeric. Let's use Float to match raw Kaggle float IDs initially. Actually, best practice is Integer or String for CustomerID. We'll use Float to match Pandas read without coercion, or Integer. Let's use Float here to be safe with Pandas NaNs if they sneak through, though we filter them. Let's use Integer and ensure we cast in pandas.
    
    # Feature engineering columns (added during ETL)
    DayOfWeek = Column(Integer)
    Month = Column(Integer)
    IsWeekend = Column(Integer)

    # Relationship to product
    product = relationship("Product", back_populates="transactions")
