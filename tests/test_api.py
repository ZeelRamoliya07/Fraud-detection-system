"""
Integration and Unit Tests for FastAPI Fraud Detection REST API.
"""

import pytest
from fastapi.testclient import TestClient
from api.main import app
from api.predictor import FraudPredictor
from src.config import OPTIMAL_THRESHOLD


@pytest.fixture
def client():
    """FastAPI TestClient fixture."""
    with TestClient(app) as c:
        yield c


@pytest.fixture
def valid_payload():
    """Valid 30-feature transaction payload."""
    payload = {"Time": 406.0, "Amount": 100.0}
    for i in range(1, 29):
        payload[f"V{i}"] = 0.0
    return payload


def test_health_endpoint(client):
    """Test GET /health returns 200 and healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_predict_endpoint_valid(client, valid_payload):
    """Test POST /predict with valid transaction payload returns 200 and expected schema."""
    response = client.post("/predict", json=valid_payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "fraud_probability" in data
    assert "is_fraud" in data
    assert "risk_level" in data
    assert "threshold" in data
    
    assert 0.0 <= data["fraud_probability"] <= 1.0
    assert data["threshold"] == OPTIMAL_THRESHOLD
    assert data["is_fraud"] == (data["fraud_probability"] >= OPTIMAL_THRESHOLD)
    assert data["risk_level"] in ["LOW", "MEDIUM", "HIGH"]


def test_predict_endpoint_negative_amount(client, valid_payload):
    """Test POST /predict with negative Amount is rejected with HTTP 422."""
    invalid = valid_payload.copy()
    invalid["Amount"] = -10.0
    response = client.post("/predict", json=invalid)
    assert response.status_code == 422


def test_predict_endpoint_negative_time(client, valid_payload):
    """Test POST /predict with negative Time is rejected with HTTP 422."""
    invalid = valid_payload.copy()
    invalid["Time"] = -5.0
    response = client.post("/predict", json=invalid)
    assert response.status_code == 422


def test_predict_endpoint_missing_feature(client, valid_payload):
    """Test POST /predict with missing feature field returns HTTP 422."""
    invalid = valid_payload.copy()
    del invalid["V14"]
    response = client.post("/predict", json=invalid)
    assert response.status_code == 422


def test_predict_endpoint_non_numeric_feature(client, valid_payload):
    """Test POST /predict with non-numeric value returns HTTP 422."""
    invalid = valid_payload.copy()
    invalid["Amount"] = "one_hundred"
    response = client.post("/predict", json=invalid)
    assert response.status_code == 422


def test_risk_level_mapping():
    """Test FraudPredictor.get_risk_level maps probabilities accurately."""
    assert FraudPredictor.get_risk_level(0.10) == "LOW"
    assert FraudPredictor.get_risk_level(0.299) == "LOW"
    assert FraudPredictor.get_risk_level(0.30) == "MEDIUM"
    assert FraudPredictor.get_risk_level(0.699) == "MEDIUM"
    assert FraudPredictor.get_risk_level(0.70) == "HIGH"
    assert FraudPredictor.get_risk_level(0.95) == "HIGH"


def test_fraud_predictor_initialization():
    """Test FraudPredictor loads serialized Random Forest model successfully."""
    predictor = FraudPredictor()
    assert predictor.pipeline is not None
    assert predictor.threshold == OPTIMAL_THRESHOLD
