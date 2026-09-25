"""
FastAPI REST API Main Entry Point for Fraud Detection System.

Exposes real-time fraud prediction and health monitoring REST endpoints with CORS support.
"""

from contextlib import asynccontextmanager
from typing import Dict, Any
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from api.schemas import TransactionInput, PredictionResponse, HealthResponse
from api.predictor import FraudPredictor

# Global predictor instance initialized during application startup
predictor: FraudPredictor = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler loading the model pipeline once during application startup.
    """
    global predictor
    try:
        predictor = FraudPredictor()
    except Exception as e:
        print(f"Error loading FraudPredictor during startup: {e}")
    yield


app = FastAPI(
    title="Fraud Detection System API",
    description=(
        "REST API for real-time financial transaction fraud detection. "
        "Evaluates 30 transaction features using a trained Random Forest pipeline "
        "and applies an optimized probability threshold (0.70) for classification."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Explicit CORS configuration for frontend development servers
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="API Health Check",
    description="Lightweight health check endpoint verifying that the service is running."
)
def health_check() -> Dict[str, str]:
    return {"status": "healthy"}


@app.post(
    "/predict",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Evaluate Fraud Risk for Transaction",
    description=(
        "Accepts 30 transaction features (Time, V1..V28, Amount), passes them through "
        "the serialized RobustScaler + Random Forest pipeline, and returns the estimated "
        "fraud probability, binary fraud decision (at threshold 0.70), and risk level."
    )
)
def predict_fraud(transaction: TransactionInput) -> Dict[str, Any]:
    global predictor
    if predictor is None:
        try:
            predictor = FraudPredictor()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Model service uninitialized: {str(e)}"
            )

    try:
        input_data = transaction.model_dump()
        result = predictor.predict(input_data)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference execution failed: {str(e)}"
        )
