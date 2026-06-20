# PROJECT BLUEPRINT: Automated Dynamic Supply-Demand Optimizer

## 1. System Architecture  
[Frontend: React/Tailwind] <---> (REST API) <---> [Backend: FastAPI]
                                                       |
                                        +--------------+--------------+
                                        |                             |
                                [DB: PostgreSQL]              [ML Pipeline]
                              (Transactional Logs)        (Scikit-Learn/Joblib) 

## 2. Current File Tree & Project Structure
supply-demand-optimizer/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # System Entrypoint (FastAPI initialization)
│   │   ├── database.py          # SQLAlchemy PostgreSQL connection engine
│   │   ├── models.py            # Database tables schema mapping
│   │   ├── schemas.py           # Pydantic data validation schemas
│   │   └── api/
│   │       └── endpoints.py     # Analytics & Optimization API routes
│   ├── ml/
│   │   ├── __init__.py
│   │   ├── train.py             # Feature engineering & Model training script
│   │   ├── predict.py           # Real-time inference wrapper
│   │   └── artifacts/           # Serialized models (.joblib files)
│   ├── data_loader.py           # ETL Pipeline (Kaggle CSV -> Cleaned PostgreSQL)
│   └── requirements.txt         # Core Python dependencies
├── frontend/                    # Future Phase
└── PROJECT_BLUEPRINT.md         # This file (Context Architecture)

## 3. Technology Stack & Dataset Reference
- Backend: Python 3.12, FastAPI, SQLAlchemy, Pydantic, Uvicorn
- Database: PostgreSQL (Local or Dockerized instance)
- Machine Learning: Pandas, NumPy, Scikit-Learn (Random Forest, Gradient Boosting), Joblib
- Selected Dataset: E-Commerce Data from UK Retailer (Kaggle URL: https://www.kaggle.com/datasets/carrie1/ecommerce-data)
- Key Fields Used: InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID

## 4. Current State & Implementation Plan
- [x] PHASE 1: Data Strategy, ETL Pipelines, and Core Database Setup (COMPLETED)
- [x] PHASE 2: Machine Learning Pipeline & Model Training (Demand & Price Elasticity) (COMPLETED)
- [x] PHASE 3: Backend REST API Development (FastAPI + Business Logic Guardrails) (COMPLETED)
- [x] PHASE 4: Frontend Dashboard Engineering (React + Tailwind + Recharts) (COMPLETED)

## 5. Completed Tasks & Modifications Log
- [2026-06-17]: Project initialized. Architecture locked down. Dataset selected.
- [2026-06-19]: **Phase 1 Completed**. Dependencies installed via Python 3.12. PostgreSQL schema established via SQLAlchemy (`app/models.py`). `data_loader.py` ETL script successfully loaded ~400k cleaned transactions.
- [2026-06-19]: **Phase 2 Started**. Implementation plan approved for Daily Product-Level Demand forecasting using `RandomForestRegressor`. Creating ML training and inference scripts.
- [2026-06-20]: **Phase 2 Completed**. SQL JOIN query patched. Trained RandomForestRegressor on 220,152 aggregated product records (MAE: 13.40, R2: 0.25). Model serialized to `.joblib` and inference engine (`predict.py`) built.
- [2026-06-20]: **Phase 3 Completed**. Built FastAPI application (`app/main.py`) with comprehensive endpoints (`app/api/endpoints.py`) including product listings, aggregate KPI analytics, and live ML inference wrappers. Uvicorn dev server is running!
- [2026-06-20]: **Phase 4 Completed**. Scaffolded Vite React application (`frontend/`). Installed Tailwind CSS v4, Recharts, and Axios. Built `KPISummary`, `PredictionPanel`, and `RevenueChart` components with a premium glassmorphism dark/light hybrid theme. Frontend is live on port 5173 and connected to the FastAPI backend.

## 6. How to Run the Project

To start the application from scratch, you will need two separate terminal windows (one for the backend, one for the frontend).

### 1. Start the Backend (Terminal 1)
Navigate to the `backend` directory, activate the virtual environment, and start the FastAPI server using Uvicorn.
```bash
cd backend
.\venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
*The backend API will be available at http://localhost:8000 (and docs at http://localhost:8000/docs).*

### 2. Start the Frontend (Terminal 2)
Navigate to the `frontend` directory and start the Vite React development server.
```bash
cd frontend
npm run dev
```
*The frontend dashboard will be available at http://localhost:5173.*