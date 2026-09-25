"""
Unit Tests for Baseline Model Pipeline and Evaluation Module.
"""

import pytest
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from src.models.baseline import build_baseline_pipeline, train_baseline_model
from src.models.evaluate import evaluate_predictions, evaluate_model, compare_evaluation_results


@pytest.fixture
def sample_dataset():
    """Generates synthetic dataset for testing baseline training and evaluation."""
    np.random.seed(42)
    n = 100
    data = {
        'Time': np.random.uniform(0, 100000, n),
        'Amount': np.random.exponential(50, n)
    }
    for i in range(1, 29):
        data[f'V{i}'] = np.random.normal(0, 1, n)
    data['Class'] = np.array([0] * 85 + [1] * 15)
    
    df = pd.DataFrame(data)
    X = df.drop(columns=['Class'])
    y = df['Class']
    return X, y


def test_build_baseline_pipeline():
    """Verify build_baseline_pipeline constructs a valid scikit-learn Pipeline."""
    pipeline = build_baseline_pipeline(class_weight='balanced', random_state=42)
    assert isinstance(pipeline, Pipeline)
    assert 'preprocessor' in pipeline.named_steps
    assert 'classifier' in pipeline.named_steps


def test_train_baseline_model(sample_dataset):
    """Verify model can fit on small training sample and return predictions."""
    X, y = sample_dataset
    pipeline = train_baseline_model(X, y, class_weight=None, random_state=42)
    
    preds = pipeline.predict(X)
    probas = pipeline.predict_proba(X)
    
    assert len(preds) == len(X)
    assert probas.shape == (len(X), 2)
    # Check probability bounds
    assert np.all(probas >= 0.0) and np.all(probas <= 1.0)
    assert np.allclose(probas.sum(axis=1), 1.0)


def test_evaluate_model(sample_dataset):
    """Verify evaluate_model calculates expected metric structure."""
    X, y = sample_dataset
    pipeline = train_baseline_model(X, y, class_weight='balanced', random_state=42)
    
    eval_results = evaluate_model(pipeline, X, y, model_name="Test Model")
    
    assert eval_results['model_name'] == "Test Model"
    assert 'precision' in eval_results
    assert 'recall' in eval_results
    assert 'f1_score' in eval_results
    assert 'pr_auc' in eval_results
    assert 'roc_auc' in eval_results
    assert 'confusion_matrix' in eval_results
    
    cm = eval_results['confusion_matrix']
    assert cm.shape == (2, 2)
    assert eval_results['tp'] + eval_results['tn'] + eval_results['fp'] + eval_results['fn'] == len(X)


def test_compare_evaluation_results(sample_dataset):
    """Verify comparison function outputs a clean pandas DataFrame."""
    X, y = sample_dataset
    p1 = train_baseline_model(X, y, class_weight=None)
    p2 = train_baseline_model(X, y, class_weight='balanced')
    
    e1 = evaluate_model(p1, X, y, model_name="Model 1")
    e2 = evaluate_model(p2, X, y, model_name="Model 2")
    
    df_comp = compare_evaluation_results([e1, e2])
    assert isinstance(df_comp, pd.DataFrame)
    assert len(df_comp) == 2
    assert "PR-AUC" in df_comp.columns
    assert "ROC-AUC" in df_comp.columns
