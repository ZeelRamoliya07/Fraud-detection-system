"""
Pydantic Schemas for Fraud Detection System REST API.

Defines strict input request validation for 30 transaction features
and structured prediction response objects.
"""

from typing import Literal
from pydantic import BaseModel, Field


class TransactionInput(BaseModel):
    """
    Transaction input schema for fraud prediction requests.
    Validates presence of 30 transaction features with bounds checks.
    """
    Time: float = Field(..., ge=0.0, description="Seconds elapsed since the first transaction in the dataset.")
    V1: float = Field(..., description="PCA principal component 1.")
    V2: float = Field(..., description="PCA principal component 2.")
    V3: float = Field(..., description="PCA principal component 3.")
    V4: float = Field(..., description="PCA principal component 4.")
    V5: float = Field(..., description="PCA principal component 5.")
    V6: float = Field(..., description="PCA principal component 6.")
    V7: float = Field(..., description="PCA principal component 7.")
    V8: float = Field(..., description="PCA principal component 8.")
    V9: float = Field(..., description="PCA principal component 9.")
    V10: float = Field(..., description="PCA principal component 10.")
    V11: float = Field(..., description="PCA principal component 11.")
    V12: float = Field(..., description="PCA principal component 12.")
    V13: float = Field(..., description="PCA principal component 13.")
    V14: float = Field(..., description="PCA principal component 14.")
    V15: float = Field(..., description="PCA principal component 15.")
    V16: float = Field(..., description="PCA principal component 16.")
    V17: float = Field(..., description="PCA principal component 17.")
    V18: float = Field(..., description="PCA principal component 18.")
    V19: float = Field(..., description="PCA principal component 19.")
    V20: float = Field(..., description="PCA principal component 20.")
    V21: float = Field(..., description="PCA principal component 21.")
    V22: float = Field(..., description="PCA principal component 22.")
    V23: float = Field(..., description="PCA principal component 23.")
    V24: float = Field(..., description="PCA principal component 24.")
    V25: float = Field(..., description="PCA principal component 25.")
    V26: float = Field(..., description="PCA principal component 26.")
    V27: float = Field(..., description="PCA principal component 27.")
    V28: float = Field(..., description="PCA principal component 28.")
    Amount: float = Field(..., ge=0.0, description="Transaction dollar amount.")

    model_config = {
        "json_schema_extra": {
            "example": {
                "Time": 406.0,
                "V1": -2.3122, "V2": 1.9519, "V3": -1.6098, "V4": 3.9979, "V5": -0.5221,
                "V6": -1.4265, "V7": -2.5373, "V8": 1.3916, "V9": -2.7700, "V10": -2.7722,
                "V11": 3.2020, "V12": -2.8999, "V13": -0.5952, "V14": -4.2892, "V15": 0.3897,
                "V16": -1.1407, "V17": -2.8300, "V18": -0.0168, "V19": 0.4169, "V20": 0.1269,
                "V21": 0.5172, "V22": -0.0350, "V23": -0.4652, "V24": 0.3201, "V25": 0.0445,
                "V26": 0.1778, "V27": 0.2611, "V28": -0.1432,
                "Amount": 0.0
            }
        }
    }


class PredictionResponse(BaseModel):
    """
    Prediction response schema containing probability, binary classification,
    application-level risk level, and threshold.
    """
    fraud_probability: float = Field(..., ge=0.0, le=1.0, description="Estimated probability of transaction fraud.")
    is_fraud: bool = Field(..., description="True if fraud_probability >= threshold; False otherwise.")
    risk_level: Literal["LOW", "MEDIUM", "HIGH"] = Field(..., description="Application-level risk classification based on probability.")
    threshold: float = Field(..., description="Decision probability threshold used for classification (0.70).")


class HealthResponse(BaseModel):
    """Health check response schema."""
    status: str = Field(..., json_schema_extra={"example": "healthy"})
