import os
import zipfile
import pandas as pd
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import Product, Transaction
from tqdm import tqdm
import time

# Create database tables if they don't exist
print("Creating database tables...")
Base.metadata.create_all(bind=engine)

DATA_ZIP_PATH = r"f:\Dynamic Supply Demand\data.csv.zip"
CSV_FILE_NAME = "data.csv"
CHUNK_SIZE = 50000

def extract_data():
    """Extracts the CSV file from the ZIP archive if needed."""
    # Assuming the zip contains data.csv
    # In pandas we can read directly from zip if we know the filename, or just pass the zip path
    # But let's be explicit and read directly using compression='zip'
    return DATA_ZIP_PATH

def process_and_load_data(zip_path: str):
    """Reads the CSV, cleans data, engineers features, and loads into PostgreSQL."""
    print(f"Reading data from {zip_path}...")
    
    # We will process in chunks to avoid blowing up memory and manage DB inserts
    db: Session = SessionLocal()
    
    try:
        # 1. Read the data directly from the zip file
        # The Kaggle dataset encoding is often 'ISO-8859-1' or 'unicode_escape'
        iterator = pd.read_csv(
            zip_path, 
            compression='zip', 
            encoding='ISO-8859-1',
            chunksize=CHUNK_SIZE
        )
        
        total_rows_inserted = 0
        
        for i, chunk in enumerate(iterator):
            print(f"Processing chunk {i+1}...")
            
            # --- 2. Data Cleaning ---
            # Drop rows missing CustomerID
            chunk = chunk.dropna(subset=['CustomerID'])
            
            # Filter out returns (Quantity <= 0) and free items / anomalies (UnitPrice <= 0)
            chunk = chunk[(chunk['Quantity'] > 0) & (chunk['UnitPrice'] > 0)]
            
            # Convert InvoiceDate to datetime
            chunk['InvoiceDate'] = pd.to_datetime(chunk['InvoiceDate'])
            
            # --- 3. Feature Engineering ---
            chunk['DayOfWeek'] = chunk['InvoiceDate'].dt.dayofweek
            chunk['Month'] = chunk['InvoiceDate'].dt.month
            chunk['IsWeekend'] = chunk['DayOfWeek'].apply(lambda x: 1 if x >= 5 else 0)
            
            # --- 4. Database Loading ---
            
            # Separate Products and Transactions
            # Get unique products in this chunk to upsert/insert
            products_chunk = chunk[['StockCode', 'Description', 'UnitPrice']].drop_duplicates(subset=['StockCode'])
            
            for _, row in products_chunk.iterrows():
                # Check if product exists to avoid IntegrityError on duplicate StockCode
                # For a massive ETL, a bulk merge/upsert is better, but this works for chunked processing
                # We do a simple 'get or create' logic here or rely on bulk insert with ignore (dialect specific)
                # Let's do a basic existence check to keep it dialect-agnostic
                existing_product = db.query(Product).filter(Product.StockCode == row['StockCode']).first()
                if not existing_product:
                    new_product = Product(
                        StockCode=row['StockCode'],
                        Description=str(row['Description'])[:255] if pd.notna(row['Description']) else "Unknown",
                        UnitPrice=float(row['UnitPrice'])
                    )
                    db.add(new_product)
            
            # Commit products first so transactions have valid foreign keys
            db.commit()
            
            # Prepare transactions
            transactions_data = []
            for _, row in chunk.iterrows():
                transaction = Transaction(
                    InvoiceNo=str(row['InvoiceNo']),
                    StockCode=str(row['StockCode']),
                    Quantity=int(row['Quantity']),
                    InvoiceDate=row['InvoiceDate'].to_pydatetime(),
                    CustomerID=float(row['CustomerID']),
                    DayOfWeek=int(row['DayOfWeek']),
                    Month=int(row['Month']),
                    IsWeekend=int(row['IsWeekend'])
                )
                transactions_data.append(transaction)
            
            # Bulk save transactions
            db.bulk_save_objects(transactions_data)
            db.commit()
            
            total_rows_inserted += len(transactions_data)
            print(f"Inserted {len(transactions_data)} transactions in chunk {i+1}.")
            
    except Exception as e:
        print(f"Error during ETL: {e}")
        db.rollback()
    finally:
        db.close()
        
    print(f"ETL Complete! Total valid transactions inserted: {total_rows_inserted}")

if __name__ == "__main__":
    start_time = time.time()
    zip_path = extract_data()
    process_and_load_data(zip_path)
    print(f"Elapsed time: {time.time() - start_time:.2f} seconds")
