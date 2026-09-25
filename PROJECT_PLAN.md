# Project Plan & Roadmap — Fraud Detection System

This document outlines the detailed 11-phase development roadmap for the **Fraud Detection System**.

---

## Phase 1 — Project Foundation

- **Status:** Completed [x]
- **Objective:** Establish a clean, standardized, and modular project directory structure, dependencies, and documentation.
- **Main Tasks:**
  - Create directory layout (`data/`, `notebooks/`, `src/`, `api/`, `models/`, `tests/`).
  - Configure `requirements.txt` with foundational dependencies.
  - Set up `.gitignore` and `.env.example`.
  - Create `README.md` and `PROJECT_PLAN.md`.
  - Initialize Python virtual environment.
- **Expected Output:** Fully structured workspace ready for data analysis and model development.

---

## Phase 2 — Dataset & Exploratory Data Analysis (EDA)

- **Status:** Completed [x]
- **Objective:** Acquire the transaction dataset and analyze its statistical properties, feature distributions, and anomaly patterns.
- **Main Tasks:**
  - Ingest raw dataset into `data/raw/creditcard.csv`.
  - Perform univariate and multivariate data exploration in `notebooks/01_eda.ipynb`.
  - Inspect class imbalance ratio (fraud vs. non-fraud).
  - Analyze feature correlations, distributions, missing values, and outliers.
- **Expected Output:** Comprehensive EDA notebook with visualizations and data insights.

---

## Phase 3 — Data Preprocessing & Feature Engineering

- **Status:** Completed [x]
- **Objective:** Clean raw data, handle duplicates, scale features, prevent data leakage, and build modular preprocessing pipelines.
- **Main Tasks:**
  - Analyze duplicate rows (1,081 duplicates: 1,062 Legitimate, 19 Fraud).
  - Build data validation and schema checking functions in `src/data/preprocessing.py`.
  - Implement feature/target separation (`Class` target).
  - Perform 80/20 stratified train/test split to preserve class imbalance.
  - Build Scikit-Learn compatible `FraudDataPreprocessor` (`RobustScaler` for `Time` & `Amount`, passthrough for `V1-V28`).
  - Fit preprocessor strictly on training data to prevent data leakage.
  - Write automated pytest suite in `tests/test_preprocessing.py`.
- **Expected Output:** Reusable preprocessing module, leakage-free train/test split pipeline, and passing test suite.

---

## Phase 4 — Baseline Model

- **Status:** Planned [ ]
- **Objective:** Build a simple, interpretable baseline model to establish benchmark performance metrics.
- **Main Tasks:**
  - Train a baseline Classifier (e.g., Logistic Regression) in `notebooks/02_baseline_model.ipynb`.
  - Evaluate baseline performance using Confusion Matrix, Precision, Recall, F1-Score, and ROC-AUC.
  - Implement basic model training script in `src/models/train.py`.
- **Expected Output:** Baseline performance metrics and a benchmark model checkpoint.

---

## Phase 5 — Model Comparison & Selection

- **Status:** Planned [ ]
- **Objective:** Train and systematically evaluate multiple candidate ML models to identify the best performer.
- **Main Tasks:**
  - Train algorithms including Decision Trees, Random Forests, and Gradient Boosting models.
  - Experiment with imbalance handling techniques (e.g., class weight adjustment, SMOTE/undersampling if applicable).
  - Perform hyperparameter tuning using cross-validation.
  - Compare models across PR-AUC, Recall, Precision, and ROC-AUC metrics.
- **Expected Output:** Comparative model evaluation report and selection of the champion algorithm.

---

## Phase 6 — Final Model & Evaluation

- **Status:** Planned [ ]
- **Objective:** Train the final chosen model on complete training data and validate on held-out test data.
- **Main Tasks:**
  - Finalize hyperparameters for the top-performing model.
  - Evaluate model performance on the unseen test set.
  - Generate final performance plots (ROC Curve, Precision-Recall Curve, Confusion Matrix).
  - Serialize model pipeline and metadata artifact into `models/fraud_detection_model.joblib`.
- **Expected Output:** Serialized production model artifact and comprehensive evaluation metrics.

---

## Phase 7 — Prediction Pipeline

- **Status:** Planned [ ]
- **Objective:** Build an end-to-end programmatic inference pipeline for single and batch predictions.
- **Main Tasks:**
  - Create prediction handler in `src/models/predict.py`.
  - Implement pipeline loading, input validation, feature transformation, and model scoring.
  - Verify prediction outputs and probability scores on sample inputs.
- **Expected Output:** Clean, reusable Python prediction API for programmatic execution.

---

## Phase 8 — FastAPI Integration

- **Status:** Planned [ ]
- **Objective:** Expose the fraud detection model via a performant REST API.
- **Main Tasks:**
  - Define input/output schema models using Pydantic in `api/schemas.py`.
  - Build endpoints (`/health`, `/predict`, `/batch-predict`) in `api/main.py`.
  - Implement request validation, error handling, and API logging.
  - Test API endpoints locally using Uvicorn.
- **Expected Output:** Fully operational FastAPI backend with interactive Swagger documentation.

---

## Phase 9 — Frontend Integration

- **Status:** Planned [ ]
- **Objective:** Build a user-facing dashboard/interface to demonstrate live transaction scoring.
- **Main Tasks:**
  - Design an interactive web interface for inputting transaction details.
  - Connect interface components to the FastAPI endpoint.
  - Display fraud probability scores, risk classification, and transaction metrics.
- **Expected Output:** Interactive web interface for real-time fraud prediction visualization.

---

## Phase 10 — Testing & Quality Assurance

- **Status:** Planned [ ]
- **Objective:** Ensure project robustness through automated unit and integration tests.
- **Main Tasks:**
  - Write unit tests for data preprocessing and feature transformations in `tests/test_preprocessing.py`.
  - Write unit tests for prediction pipeline in `tests/test_prediction.py`.
  - Write API endpoint integration tests using FastAPI `TestClient` in `tests/test_api.py`.
  - Run pytest suite and verify code quality.
- **Expected Output:** Comprehensive test suite passing with high coverage.

---

## Phase 11 — Documentation & Deployment

- **Status:** Planned [ ]
- **Objective:** Finalize project documentation and deployment instructions.
- **Main Tasks:**
  - Update `README.md` with final results, evaluation metrics, and API instructions.
  - Document technical interview talking points and architectural decisions.
  - Prepare repository for public portfolio presentation.
- **Expected Output:** Complete portfolio-grade open-source project repository.
