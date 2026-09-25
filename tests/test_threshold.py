"""
Unit Tests for Decision Threshold Optimization Module.
"""

import pytest
import numpy as np
import pandas as pd
from src.models.threshold import evaluate_threshold, evaluate_threshold_sweep, select_optimal_threshold


@pytest.fixture
def sample_predictions():
    """Generates synthetic ground truth and probability predictions."""
    np.random.seed(42)
    n = 200
    y_true = np.array([0] * 170 + [1] * 30)
    # Synthetic probabilities (correlated with class)
    y_proba = np.where(y_true == 1, np.random.uniform(0.4, 0.95, n), np.random.uniform(0.05, 0.6, n))
    return y_true, y_proba


def test_evaluate_threshold_valid(sample_predictions):
    """Verify evaluate_threshold returns correct dictionary structure and valid ranges."""
    y_true, y_proba = sample_predictions
    res = evaluate_threshold(y_true, y_proba, threshold=0.50)

    assert isinstance(res, dict)
    expected_keys = {'threshold', 'precision', 'recall', 'f1_score', 'accuracy', 'tp', 'tn', 'fp', 'fn'}
    assert expected_keys.issubset(set(res.keys()))

    # Check metric ranges
    assert 0.0 <= res['precision'] <= 1.0
    assert 0.0 <= res['recall'] <= 1.0
    assert 0.0 <= res['f1_score'] <= 1.0
    assert 0.0 <= res['accuracy'] <= 1.0

    # Internal consistency check
    total_samples = res['tp'] + res['tn'] + res['fp'] + res['fn']
    assert total_samples == len(y_true)


def test_evaluate_threshold_invalid_range(sample_predictions):
    """Verify threshold evaluation raises ValueError for invalid thresholds outside [0, 1]."""
    y_true, y_proba = sample_predictions
    with pytest.raises(ValueError, match="Threshold must be between 0.0 and 1.0"):
        evaluate_threshold(y_true, y_proba, threshold=1.5)

    with pytest.raises(ValueError, match="Threshold must be between 0.0 and 1.0"):
        evaluate_threshold(y_true, y_proba, threshold=-0.1)


def test_evaluate_threshold_mismatched_lengths(sample_predictions):
    """Verify threshold evaluation raises ValueError when array lengths mismatch."""
    y_true, y_proba = sample_predictions
    with pytest.raises(ValueError, match="Array length mismatch"):
        evaluate_threshold(y_true[:100], y_proba, threshold=0.5)


def test_evaluate_threshold_sweep(sample_predictions):
    """Verify threshold sweep produces requested thresholds and expected DataFrame format."""
    y_true, y_proba = sample_predictions
    custom_thresholds = [0.20, 0.50, 0.70]
    df_sweep = evaluate_threshold_sweep(y_true, y_proba, thresholds=custom_thresholds)

    assert isinstance(df_sweep, pd.DataFrame)
    assert len(df_sweep) == 3
    assert list(df_sweep['Threshold']) == custom_thresholds

    required_cols = {'Threshold', 'Precision', 'Recall', 'F1-Score', 'Accuracy', 'TP', 'FN', 'FP', 'TN'}
    assert required_cols.issubset(set(df_sweep.columns))


def test_select_optimal_threshold(sample_predictions):
    """Verify optimal threshold selection via max F1 strategy."""
    y_true, y_proba = sample_predictions
    df_sweep = evaluate_threshold_sweep(y_true, y_proba)

    best_res = select_optimal_threshold(df_sweep, strategy='f1')
    assert isinstance(best_res, dict)
    assert 'Threshold' in best_res
    assert 'F1-Score' in best_res
    assert best_res['F1-Score'] == df_sweep['F1-Score'].max()
