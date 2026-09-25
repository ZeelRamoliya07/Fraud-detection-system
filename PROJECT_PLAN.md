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

- **Status:** Completed [x]
- **Objective:** Build and evaluate Logistic Regression as the baseline classification model under unweighted and class-weighted configurations.
- **Main Tasks:**
  - Build baseline model pipeline constructor in `src/models/baseline.py`.
  - Build evaluation module (`src/models/evaluate.py`) calculating Precision, Recall, F1, PR-AUC, ROC-AUC, and Confusion Matrices.
  - Train Experiment A (`LogisticRegression`, `class_weight=None`).
  - Train Experiment B (`LogisticRegression`, `class_weight='balanced'`).
  - Evaluate both experiments on held-out test data in `notebooks/02_baseline_model.ipynb`.
  - Serialize baseline pipelines to `models/logistic_regression_baseline.joblib` and `models/logistic_regression_balanced.joblib`.
  - Write unit tests in `tests/test_baseline.py`.
- **Expected Output:** Serialized baseline pipelines, comparison table, confusion matrices, PR/ROC curves, and passing test suite.

---

## Phase 5 — Model Comparison & Selection

- **Status:** Completed [x]
- **Objective:** Train and systematically evaluate non-linear tree-based models (Decision Tree and Random Forest) against Phase 4 baselines.
- **Main Tasks:**
  - Create tree model pipeline builders in `src/models/trees.py`.
  - Train `DecisionTreeClassifier(class_weight='balanced', max_depth=10)`.
  - Train `RandomForestClassifier(n_estimators=100, class_weight='balanced', max_depth=10)`.
  - Compare 4 model configurations on held-out test data in `notebooks/03_model_comparison.ipynb`.
  - Extract feature importance rankings (`feature_importances_`) for model interpretability.
  - Serialize tree pipelines to `models/decision_tree.joblib` and `models/random_forest.joblib`.
  - Write unit test suite in `tests/test_trees.py`.
- **Expected Output:** Full 4-model comparison table, feature importance plots, serialized tree pipelines, and passing unit tests.

---

## Phase 6 — Decision Threshold Optimization

- **Status:** Completed [x]
- **Objective:** Optimize the probability decision boundary for the champion Random Forest pipeline without retraining.
- **Main Tasks:**
  - Build threshold optimization utilities (`src/models/threshold.py`) and central configuration (`src/config.py`).
  - Load `models/random_forest.joblib` and predict continuous test probabilities `predict_proba(X_test)[:, 1]`.
  - Conduct threshold sweep across probabilities `0.10` to `0.90` in `notebooks/04_threshold_optimization.ipynb`.
  - Analyze trade-offs between Precision, Recall, F1-Score, False Positives, and False Negatives.
  - Select optimal operational threshold (`0.70`, achieving **F1 = 0.8046**, **Precision = 88.61%**, **Recall = 73.68%**, and reducing False Positives from 24 to 9).
  - Write unit tests in `tests/test_threshold.py`.
- **Expected Output:** Threshold sweep DataFrame, trade-off visualizations, operational threshold rationale, config constant `OPTIMAL_THRESHOLD = 0.70`, and passing unit test suite.

---

## Phase 7 — FastAPI Prediction API

- **Status:** Completed [x]
- **Objective:** Build a performant, validated REST API exposing the trained Random Forest pipeline with threshold-aware risk scoring.
- **Main Tasks:**
  - Define input/output schemas in `api/schemas.py` using Pydantic (30 input features, non-negative Amount/Time validation).
  - Build `FraudPredictor` component in `api/predictor.py` loading `models/random_forest.joblib` once at startup and applying `OPTIMAL_THRESHOLD = 0.70`.
  - Build FastAPI application in `api/main.py` with `GET /health` and `POST /predict` endpoints.
  - Map predicted probabilities to application-level risk levels (`LOW`: <0.30, `MEDIUM`: 0.30–0.70, `HIGH`: >=0.70).
  - Write comprehensive API unit & integration tests in `tests/test_api.py`.
- **Expected Output:** Fully functional REST API with Swagger documentation (`/docs`), Pydantic validation, and 29 passing unit tests.

---

## Phase 8 — React Frontend Integration

- **Status:** Completed [x]
- **Objective:** Build a clean, editorial/financial-tool React dashboard using Vite and Tailwind CSS to consume the FastAPI prediction API.
- **Main Tasks:**
  - Configure explicit CORS middleware on FastAPI backend (`api/main.py`).
  - Create React + Vite frontend application in `frontend/`.
  - Build `TransactionForm` component with feature inputs (Time, Amount, V1–V28 feature grid, reset, and preset buttons for sample fraud vs. normal transactions).
  - Build `PredictionResult` component displaying fraud probability (e.g. 88.61%), risk level badge (`LOW`, `MEDIUM`, `HIGH`), classification outcome, and decision threshold (70%).
  - Build API service module (`src/services/api.js`) consuming `VITE_API_BASE_URL`.
  - Write Vitest component unit tests (`src/test/App.test.jsx`).
- **Expected Output:** Operational React dashboard with editorial design, zero raw ML logic in frontend, 5 passing Vitest tests, and 29 passing backend pytest tests.

---

## Phase 9 — Testing & Quality Assurance

- **Status:** Planned [ ]
- **Objective:** Maintain and expand automated unit and integration tests across the codebase.
- **Main Tasks:**
  - Maintain full test coverage across backend (`pytest`) and frontend (`vitest`).
  - Execute test suite prior to deployment.
- **Expected Output:** Fully tested, production-grade application codebase.

---

## Phase 10 — Documentation & Deployment

- **Status:** Planned [ ]
- **Objective:** Finalize project documentation and deployment instructions.
- **Main Tasks:**
  - Update `README.md` with final results, evaluation metrics, and API/frontend usage instructions.
  - Document technical interview talking points and architectural decisions.
  - Prepare repository for public portfolio presentation.
- **Expected Output:** Complete portfolio-grade open-source project repository.
