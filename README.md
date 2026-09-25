# Fraud Detection System

> **Status:** Phase 7 — FastAPI Prediction API Completed  
> *Note: Phases 1–7 (Foundation, EDA, Preprocessing, Baseline Models, Tree Model Comparison, Threshold Optimization, and FastAPI Prediction API) are complete.*

## Overview

The **Fraud Detection System** is an end-to-end machine learning project designed to detect fraudulent financial transactions. It demonstrates core ML engineering fundamentals—from exploratory data analysis and feature engineering to model comparison, threshold optimization, dynamic REST API deployment with FastAPI, and automated testing.

This repository serves as Project 3 in an AI Engineering portfolio focusing on core ML fundamentals, robust system architecture, and production-ready code design.

---

## Problem Statement & Metric Justification

Financial fraud presents a critical threat to modern financial institutions, leading to billions of dollars in losses annually. Detecting fraudulent transactions presents unique machine learning challenges:
- **Severe Class Imbalance:** Fraudulent transactions constitute a minuscule fraction (~0.17%) of transaction volume (~599:1 ratio).
- **Why Accuracy is Misleading:** A trivial dummy model that predicts all transactions as legitimate achieves **99.83% accuracy** while missing **100% of fraud**.
- **Primary Metrics (PR-AUC & Recall):** Model selection relies primarily on **PR-AUC (Precision-Recall AUC)**, **Recall** (catching true fraud), and **Precision** (minimizing false customer friction).

---

## Prediction REST API (Phase 7 Implementation)

The system exposes a high-performance REST API using **FastAPI**, **Uvicorn**, and **Pydantic**. The API loads the serialized `models/random_forest.joblib` pipeline once at application startup and applies the optimized decision threshold (`0.70`).

### Starting the API Server

```bash
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Start FastAPI server with Uvicorn
uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
```

Interactive OpenAPI / Swagger Documentation is available at:
- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc UI:** `http://127.0.0.1:8000/redoc`

---

### REST API Endpoints

#### 1. `GET /health`
Lightweight health check verifying that the API service is active.

**Response `(HTTP 200 OK)`:**
```json
{
  "status": "healthy"
}
```

#### 2. `POST /predict`
Evaluates fraud probability and risk classification for a transaction payload containing 30 input features (`Time`, `V1`..`V28`, `Amount`).

**Example Request Payload:**
```json
{
  "Time": 406.0,
  "V1": -2.3122, "V2": 1.9519, "V3": -1.6098, "V4": 3.9979, "V5": -0.5221,
  "V6": -1.4265, "V7": -2.5373, "V8": 1.3916, "V9": -2.7700, "V10": -2.7722,
  "V11": 3.2020, "V12": -2.8999, "V13": -0.5952, "V14": -4.2892, "V15": 0.3897,
  "V16": -1.1407, "V17": -2.8300, "V18": -0.0168, "V19": 0.4169, "V20": 0.1269,
  "V21": 0.5172, "V22": -0.0350, "V23": -0.4652, "V24": 0.3201, "V25": 0.0445,
  "V26": 0.1778, "V27": 0.2611, "V28": -0.1432,
  "Amount": 100.0
}
```

**Example Response Payload `(HTTP 200 OK)`:**
```json
{
  "fraud_probability": 0.83,
  "is_fraud": true,
  "risk_level": "HIGH",
  "threshold": 0.70
}
```

### Risk Level Mapping:
- **`LOW`**: Fraud Probability < `0.30`
- **`MEDIUM`**: `0.30` <= Fraud Probability < `0.70`
- **`HIGH`**: Fraud Probability >= `0.70`

---

## Decision Threshold Optimization (Phase 6 Results)

Evaluated on unseen test set (`56,746` transactions) using continuous probabilities from our champion **Random Forest** pipeline:

| Threshold | Precision | Recall | F1-Score | Accuracy | TP (Fraud Caught) | FN (Fraud Missed) | FP (False Alarms) | TN (Legit Correct) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 0.50 *(Default)* | 0.7526 | 0.7684 | 0.7604 | 99.92% | 73 | 22 | 24 | 56,627 |
| **0.70 (Selected)** | **0.8861** | **0.7368** | **0.8046** | **99.94%** | **70** | **25** | **9** | **56,642** |

---

## Architecture & Module Layout

```
fraud-detection-system/
│
├── api/                   # REST API package
│   ├── __init__.py
│   ├── main.py            # FastAPI entry point (/health, /predict)
│   ├── predictor.py       # Model inference service component
│   └── schemas.py         # Pydantic request & response schemas
│
├── data/                  # Data directory
│   ├── raw/               # Raw transaction dataset (creditcard.csv)
│   └── processed/         # Processed datasets
│
├── notebooks/             # Jupyter notebooks
│   ├── 01_eda.ipynb       # Phase 2 Exploratory Data Analysis
│   ├── 02_baseline_model.ipynb # Phase 4 Baseline Model Experiments
│   ├── 03_model_comparison.ipynb # Phase 5 Tree Model Comparison
│   └── 04_threshold_optimization.ipynb # Phase 6 Decision Threshold Sweep
│
├── src/                   # Source code package
│   ├── __init__.py
│   ├── config.py          # Configuration constants (OPTIMAL_THRESHOLD=0.70)
│   ├── data/              # Preprocessing & validation module
│   │   ├── __init__.py
│   │   └── preprocessing.py # Preprocessing pipeline & RobustScaler transformer
│   └── models/            # Model training & evaluation modules
│       ├── __init__.py
│       ├── baseline.py    # Baseline Logistic Regression pipeline builder
│       ├── trees.py       # Decision Tree & Random Forest pipeline builders
│       ├── evaluate.py    # Metrics evaluation module
│       └── threshold.py   # Threshold sweep & decision boundary utilities
│
├── models/                # Serialized trained model pipelines (.joblib)
│   ├── logistic_regression_baseline.joblib
│   ├── logistic_regression_balanced.joblib
│   ├── decision_tree.joblib
│   └── random_forest.joblib
│
├── tests/                 # Unit and integration test suites
│   ├── test_preprocessing.py
│   ├── test_baseline.py
│   ├── test_trees.py
│   ├── test_threshold.py
│   └── test_api.py        # REST API integration & validation tests
│
├── README.md              # Project documentation overview
├── PROJECT_PLAN.md        # Detailed phase-by-phase development plan
├── requirements.txt       # Project dependency specifications
├── .gitignore             # Git ignore rules
└── .env.example           # Environment variables template
```

---

## Project Status

- [x] **Phase 1 — Project Foundation**
- [x] **Phase 2 — Dataset & Exploratory Data Analysis**
- [x] **Phase 3 — Data Preprocessing & Validation**
- [x] **Phase 4 — Baseline Machine Learning Model**
- [x] **Phase 5 — Nonlinear Model Comparison**
- [x] **Phase 6 — Decision Threshold Optimization**
- [x] **Phase 7 — FastAPI Prediction API** *(Current)*
- [ ] Phase 8 — Frontend Integration
- [ ] Phase 9 — Testing & Quality Assurance
- [ ] Phase 10 — Documentation & Deployment