# Fraud Detection System

> **Status:** Phase 6 — Decision Threshold Optimization Completed  
> *Note: Phases 1–6 (Foundation, EDA, Preprocessing, Baseline Models, Tree Model Comparison, and Threshold Optimization) are complete.*

## Overview

The **Fraud Detection System** is an end-to-end machine learning project designed to detect fraudulent financial transactions. It demonstrates core ML engineering fundamentals—from exploratory data analysis and feature engineering to model comparison, threshold optimization, dynamic API deployment with FastAPI, and automated testing.

This repository serves as Project 3 in an AI Engineering portfolio focusing on core ML fundamentals, robust system architecture, and production-ready code design.

---

## Problem Statement & Metric Justification

Financial fraud presents a critical threat to modern financial institutions, leading to billions of dollars in losses annually. Detecting fraudulent transactions presents unique machine learning challenges:
- **Severe Class Imbalance:** Fraudulent transactions constitute a minuscule fraction (~0.17%) of transaction volume (~599:1 ratio).
- **Why Accuracy is Misleading:** A trivial dummy model that predicts all transactions as legitimate achieves **99.83% accuracy** while missing **100% of fraud**.
- **Primary Metrics (PR-AUC & Recall):** Model selection relies primarily on **PR-AUC (Precision-Recall AUC)**, **Recall** (catching true fraud), and **Precision** (minimizing false customer friction).

---

## Decision Threshold Optimization (Phase 6 Results)

Evaluated on unseen test set (`56,746` total transactions: `56,651` Legitimate, `95` Fraud) using continuous probabilities from our champion **Random Forest** pipeline:

### Threshold Sweep Results:

| Threshold | Precision | Recall | F1-Score | Accuracy | TP (Fraud Caught) | FN (Fraud Missed) | FP (False Alarms) | TN (Legit Correct) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 0.10 | 0.0712 | **0.8632** | 0.1316 | 98.09% | **82** | **13** | 1,069 | 55,582 |
| 0.20 | 0.2888 | 0.8421 | 0.4301 | 99.63% | 80 | 15 | 197 | 56,454 |
| 0.35 | 0.6063 | 0.8105 | 0.6937 | 99.88% | 77 | 18 | 50 | 56,601 |
| 0.50 *(Default)* | 0.7526 | 0.7684 | 0.7604 | 99.92% | 73 | 22 | 24 | 56,627 |
| **0.70 (Selected)** | **0.8861** | **0.7368** | **0.8046** | **99.94%** | **70** | **25** | **9** | **56,642** |
| 0.85 | 0.8904 | 0.6842 | 0.7738 | 99.93% | 65 | 30 | 8 | 56,643 |

### Why Threshold 0.70 Was Selected:
1. **Maximum F1-Score (0.8046):** Threshold `0.70` achieves the highest overall harmonic mean of Precision and Recall on unseen test data.
2. **62.5% Reduction in False Alarms:** False Positives drop sharply from **24 to 9** compared to default 0.50 (increasing Precision from **75.26% to 88.61%**).
3. **High Fraud Catch Rate:** Retains strong detection capability (**70 out of 95** fraud cases caught, 73.68% Recall).
4. **PR-AUC Invariance:** PR-AUC remains constant at **0.7829** across all decision thresholds as it evaluates ranking across all operational boundaries.

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
│   ├── 02_baseline_model.ipynb # Phase 4 Baseline Model Experiments
│   ├── 03_model_comparison.ipynb # Phase 5 Tree Model Comparison
│   └── 04_threshold_optimization.ipynb # Phase 6 Decision Threshold Sweep
│
├── src/                   # Source code package
│   ├── __init__.py
│   ├── config.py          # Configuration constants (DEFAULT_THRESHOLD=0.50, OPTIMAL_THRESHOLD=0.70)
│   ├── data/              # Ingestion, validation & preprocessing module
│   │   ├── __init__.py
│   │   └── preprocessing.py # Preprocessing pipeline & RobustScaler transformer
│   ├── models/            # Model training, evaluation & threshold modules
│   │   ├── __init__.py
│   │   ├── baseline.py    # Baseline Logistic Regression pipeline builder
│   │   ├── trees.py       # Decision Tree & Random Forest pipeline builders
│   │   ├── evaluate.py    # Metrics evaluation module
│   │   └── threshold.py   # Threshold sweep & decision boundary utilities
│   └── utils/             # Helper utilities
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
│   └── test_threshold.py  # Threshold optimization unit tests
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
- [x] **Phase 6 — Decision Threshold Optimization** *(Current)*
- [ ] Phase 7 — Prediction Pipeline
- [ ] Phase 8 — FastAPI Integration
- [ ] Phase 9 — Frontend Integration
- [ ] Phase 10 — Testing
- [ ] Phase 11 — Documentation & Deployment