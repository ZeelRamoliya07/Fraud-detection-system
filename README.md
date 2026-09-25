# Fraud Detection System

> **Status:** Phase 4 — Baseline Machine Learning Model Completed  
> *Note: Phases 1–4 (Foundation, EDA, Preprocessing, Baseline Models) are complete. Model comparison with tree ensembles will occur in Phase 5.*

## Overview

The **Fraud Detection System** is an end-to-end machine learning project designed to detect fraudulent financial transactions. It demonstrates core ML engineering fundamentals—from exploratory data analysis and feature engineering to model comparison, evaluation, dynamic API deployment with FastAPI, and automated testing.

This repository serves as Project 3 in an AI Engineering portfolio focusing on core ML fundamentals, robust system architecture, and production-ready code design.

---

## Problem Statement & Metric Justification

Financial fraud presents a critical threat to modern financial institutions, leading to billions of dollars in losses annually. Detecting fraudulent transactions presents unique machine learning challenges:
- **Severe Class Imbalance:** Fraudulent transactions constitute a minuscule fraction (~0.17%) of transaction volume (~599:1 ratio).
- **Why Accuracy is Misleading:** A trivial dummy model that predicts all transactions as legitimate achieves **99.83% accuracy** while missing **100% of fraud**.
- **Primary Metrics (PR-AUC & Recall):** Model selection relies primarily on **PR-AUC (Precision-Recall AUC)**, **Recall** (catching true fraud), and **Precision** (minimizing false customer friction).

---

## Baseline Model Performance (Phase 4 Results)

Evaluated on unseen test set (`56,746` transactions: `56,651` Legitimate, `95` Fraud):

| Model | Precision | Recall | F1-Score | PR-AUC | ROC-AUC | Accuracy | TP (Fraud Caught) | FN (Fraud Missed) | FP (False Alarms) | TN (Legit Correct) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression (Unweighted)** | **0.8615** | 0.5895 | **0.7000** | **0.6951** | 0.9575 | 99.92% | 56 | 39 | **9** | 56,642 |
| **Logistic Regression (Balanced)** | 0.0562 | **0.8737** | 0.1057 | 0.6719 | **0.9657** | 97.52% | **83** | **12** | 1,393 | 55,258 |

### Key Technical Findings:
- **Unweighted Logistic Regression:** Provides high Precision (86.15%) with very few false alarms (9 FP), but misses 39 out of 95 fraud cases (58.95% Recall).
- **Class-Weighted (`class_weight='balanced'`):** Drastically improves Recall from 58.95% to **87.37%** (catching 83 out of 95 fraud cases), but penalizing majority loss equally causes a surge in false alarms (1,393 FP), dropping Precision to 5.62%.

---

## Architecture & Module Layout

```
fraud-detection-system/
│
├── data/                  # Data directory
│   ├── raw/               # Raw transaction dataset (creditcard.csv)
│   └── processed/         # Cleaned, processed datasets
│
├── notebooks/             # Jupyter notebooks
│   ├── 01_eda.ipynb       # Phase 2 Exploratory Data Analysis
│   └── 02_baseline_model.ipynb # Phase 4 Baseline Model Experiments
│
├── src/                   # Source code package
│   ├── __init__.py
│   ├── data/              # Ingestion, validation & preprocessing module
│   │   ├── __init__.py
│   │   └── preprocessing.py # Preprocessing pipeline & RobustScaler transformer
│   ├── models/            # Model training & evaluation modules
│   │   ├── __init__.py
│   │   ├── baseline.py    # Baseline Logistic Regression pipeline builder
│   │   └── evaluate.py    # Metrics evaluation module (Precision, Recall, PR-AUC, ROC-AUC)
│   └── utils/             # Helper utilities
│
├── models/                # Serialized trained model pipelines (.joblib)
│   ├── logistic_regression_baseline.joblib
│   └── logistic_regression_balanced.joblib
│
├── tests/                 # Unit and integration test suites
│   ├── test_preprocessing.py
│   └── test_baseline.py   # Baseline model & evaluation unit tests
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
- [x] **Phase 4 — Baseline Machine Learning Model** *(Current)*
- [ ] Phase 5 — Model Comparison & Selection
- [ ] Phase 6 — Final Model & Evaluation
- [ ] Phase 7 — Prediction Pipeline
- [ ] Phase 8 — FastAPI Integration
- [ ] Phase 9 — Frontend Integration
- [ ] Phase 10 — Testing
- [ ] Phase 11 — Documentation & Deployment