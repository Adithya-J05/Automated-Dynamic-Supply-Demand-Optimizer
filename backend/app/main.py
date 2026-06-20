from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router as api_router

app = FastAPI(
    title="Automated Dynamic Supply-Demand Optimizer API",
    description="Backend REST API for Phase 3 of the project, exposing DB and ML predictions.",
    version="1.0.0"
)

# Configure CORS to allow the React frontend to make requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, change to specific frontend origins like "http://localhost:3000"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the endpoints router
app.include_router(api_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Welcome to the Supply-Demand Optimizer API. Visit /docs for the Swagger UI."}
