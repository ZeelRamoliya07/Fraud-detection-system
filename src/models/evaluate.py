"""
Evaluation Module for Fraud Detection System.

Computes comprehensive metrics (Precision, Recall, F1, PR-AUC, ROC-AUC, Confusion Matrix)
using predicted probabilities on held-out test data.
"""

from typing import Dict, Any, Tuple, Optional
import numpy as np
import pandas as pd
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    accuracy_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
    precision_recall_curve,
    roc_curve
)


def evaluate_predictions(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_proba: np.ndarray,
    model_name: str = "Model"
) -> Dict[str, Any]:
    """
    Calculates detailed evaluation metrics given ground truth, hard predictions,
    and predicted probabilities for the positive class (Fraud = 1).

    Returns:
        Dict containing all quantitative evaluation metrics and curves.
    """
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()

    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    accuracy = accuracy_score(y_true, y_pred)
    roc_auc = roc_auc_score(y_true, y_proba)
    pr_auc = average_precision_score(y_true, y_proba)

    # Compute PR and ROC curves for plotting
    precisions, recalls, pr_thresholds = precision_recall_curve(y_true, y_proba)
    fpr, tpr, roc_thresholds = roc_curve(y_true, y_proba)

    metrics = {
        'model_name': model_name,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'pr_auc': pr_auc,
        'roc_auc': roc_auc,
        'accuracy': accuracy,
        'tp': int(tp),
        'tn': int(tn),
        'fp': int(fp),
        'fn': int(fn),
        'confusion_matrix': np.array([[tn, fp], [fn, tp]]),
        'pr_curve': {'precision': precisions, 'recall': recalls, 'thresholds': pr_thresholds},
        'roc_curve': {'fpr': fpr, 'tpr': tpr, 'thresholds': roc_thresholds}
    }

    return metrics


def evaluate_model(
    model_pipeline: Any,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    model_name: str = "Model"
) -> Dict[str, Any]:
    """
    Evaluates a fitted pipeline on unseen test data.

    Returns:
        Dict of computed evaluation metrics.
    """
    # Obtain hard predictions and predicted probabilities for positive class (Class=1)
    y_pred = model_pipeline.predict(X_test)
    y_proba = model_pipeline.predict_proba(X_test)[:, 1]

    return evaluate_predictions(y_test.values, y_pred, y_proba, model_name=model_name)


def compare_evaluation_results(results_list: list) -> pd.DataFrame:
    """
    Converts a list of evaluation metric dictionaries into a clean summary DataFrame.

    Returns:
        Formatted pandas DataFrame comparing model metrics.
    """
    rows = []
    for res in results_list:
        rows.append({
            'Model': res['model_name'],
            'Precision': res['precision'],
            'Recall': res['recall'],
            'F1-Score': res['f1_score'],
            'PR-AUC': res['pr_auc'],
            'ROC-AUC': res['roc_auc'],
            'Accuracy': res['accuracy'],
            'TP (Fraud caught)': res['tp'],
            'FN (Fraud missed)': res['fn'],
            'FP (False Alarm)': res['fp'],
            'TN (Legit correct)': res['tn']
        })
    df_compare = pd.DataFrame(rows)
    return df_compare
