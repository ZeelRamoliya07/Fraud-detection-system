"""
Decision Threshold Optimization Module for Fraud Detection System.

Provides utilities for evaluating classification metrics across custom probability
thresholds, performing threshold sweeps, and selecting optimal decision boundaries.
"""

from typing import Dict, Any, List, Optional, Union
import numpy as np
import pandas as pd
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    accuracy_score,
    confusion_matrix
)
from src.config import DEFAULT_THRESHOLD, OPTIMAL_THRESHOLD


def evaluate_threshold(
    y_true: Union[np.ndarray, pd.Series],
    y_proba: Union[np.ndarray, pd.Series],
    threshold: float = 0.50
) -> Dict[str, Any]:
    """
    Evaluates classification metrics for a specific probability threshold.

    Args:
        y_true: Ground truth binary labels (0 or 1).
        y_proba: Predicted probabilities for the positive class (Fraud = 1).
        threshold: Decision boundary probability threshold in [0.0, 1.0].

    Returns:
        Dict containing precision, recall, f1_score, accuracy, tp, tn, fp, fn.

    Raises:
        ValueError: If threshold is not in [0, 1] or array lengths mismatch.
    """
    if not (0.0 <= threshold <= 1.0):
        raise ValueError(f"Threshold must be between 0.0 and 1.0, got {threshold}")

    y_true_arr = np.asarray(y_true)
    y_proba_arr = np.asarray(y_proba)

    if len(y_true_arr) != len(y_proba_arr):
        raise ValueError(f"Array length mismatch: y_true ({len(y_true_arr)}) vs y_proba ({len(y_proba_arr)})")

    y_pred = (y_proba_arr >= threshold).astype(int)

    tn, fp, fn, tp = confusion_matrix(y_true_arr, y_pred).ravel()

    precision = float(precision_score(y_true_arr, y_pred, zero_division=0))
    recall = float(recall_score(y_true_arr, y_pred, zero_division=0))
    f1 = float(f1_score(y_true_arr, y_pred, zero_division=0))
    accuracy = float(accuracy_score(y_true_arr, y_pred))

    return {
        'threshold': float(threshold),
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'accuracy': accuracy,
        'tp': int(tp),
        'tn': int(tn),
        'fp': int(fp),
        'fn': int(fn)
    }


def evaluate_threshold_sweep(
    y_true: Union[np.ndarray, pd.Series],
    y_proba: Union[np.ndarray, pd.Series],
    thresholds: Optional[List[float]] = None
) -> pd.DataFrame:
    """
    Evaluates classification performance across a range of probability thresholds.

    Args:
        y_true: Ground truth binary labels.
        y_proba: Predicted probabilities for positive class.
        thresholds: List of thresholds to evaluate. Defaults to 0.10 through 0.90 in steps of 0.05.

    Returns:
        pandas DataFrame summarizing metrics across all thresholds.
    """
    if thresholds is None:
        thresholds = [round(t, 2) for t in np.arange(0.10, 0.95, 0.05)]

    rows = []
    for t in thresholds:
        res = evaluate_threshold(y_true, y_proba, threshold=t)
        rows.append({
            'Threshold': res['threshold'],
            'Precision': res['precision'],
            'Recall': res['recall'],
            'F1-Score': res['f1_score'],
            'Accuracy': res['accuracy'],
            'TP': res['tp'],
            'FN': res['fn'],
            'FP': res['fp'],
            'TN': res['tn']
        })

    df_sweep = pd.DataFrame(rows)
    return df_sweep


def select_optimal_threshold(
    df_sweep: pd.DataFrame,
    strategy: str = 'f1',
    target_recall: Optional[float] = None
) -> Dict[str, Any]:
    """
    Selects optimal decision threshold from a threshold sweep DataFrame.

    Args:
        df_sweep: DataFrame produced by evaluate_threshold_sweep.
        strategy: 'f1' (maximizes F1-Score) or 'target_recall' (finds highest precision given target_recall).
        target_recall: Minimum required recall if strategy='target_recall'.

    Returns:
        Dict containing selected threshold and associated performance metrics.
    """
    if df_sweep.empty:
        raise ValueError("Input threshold sweep DataFrame is empty.")

    if strategy == 'f1':
        best_idx = df_sweep['F1-Score'].idxmax()
        best_row = df_sweep.loc[best_idx].to_dict()
        return best_row
    elif strategy == 'target_recall':
        if target_recall is None:
            raise ValueError("target_recall must be provided when strategy='target_recall'")
        eligible = df_sweep[df_sweep['Recall'] >= target_recall]
        if eligible.empty:
            # Fall back to max recall
            best_idx = df_sweep['Recall'].idxmax()
        else:
            best_idx = eligible['Precision'].idxmax()
        return df_sweep.loc[best_idx].to_dict()
    else:
        raise ValueError(f"Unknown strategy: '{strategy}'. Supported strategies: 'f1', 'target_recall'")
