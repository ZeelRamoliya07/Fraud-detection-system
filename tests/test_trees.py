"""
Unit Tests for Nonlinear Tree Models Module (Decision Tree & Random Forest).
"""

import pytest
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from src.models.trees import (
    build_decision_tree_pipeline,
    build_random_forest_pipeline,
    train_tree_model,
    extract_feature_importances
)
from src.models.evaluate import evaluate_model


@pytest.fixture
def sample_dataset():
    """Generates synthetic dataset for testing tree models."""
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


def test_build_decision_tree_pipeline():
    """Verify build_decision_tree_pipeline constructs a valid Pipeline."""
    pipeline = build_decision_tree_pipeline(class_weight='balanced', max_depth=5, random_state=42)
    assert isinstance(pipeline, Pipeline)
    assert 'preprocessor' in pipeline.named_steps
    assert 'classifier' in pipeline.named_steps


def test_build_random_forest_pipeline():
    """Verify build_random_forest_pipeline constructs a valid Pipeline."""
    pipeline = build_random_forest_pipeline(n_estimators=10, class_weight='balanced', max_depth=5, random_state=42)
    assert isinstance(pipeline, Pipeline)
    assert 'preprocessor' in pipeline.named_steps
    assert 'classifier' in pipeline.named_steps


def test_train_decision_tree(sample_dataset):
    """Verify Decision Tree fits on sample data, predicts valid probabilities, and yields feature importances."""
    X, y = sample_dataset
    pipeline = build_decision_tree_pipeline(max_depth=5, random_state=42)
    fitted_pipeline = train_tree_model(pipeline, X, y)
    
    preds = fitted_pipeline.predict(X)
    probas = fitted_pipeline.predict_proba(X)
    
    assert len(preds) == len(X)
    assert probas.shape == (len(X), 2)
    assert np.all(probas >= 0.0) and np.all(probas <= 1.0)
    
    eval_results = evaluate_model(fitted_pipeline, X, y, model_name="Decision Tree Test")
    assert 'pr_auc' in eval_results
    assert 'roc_auc' in eval_results
    assert eval_results['confusion_matrix'].shape == (2, 2)
    
    imp_df = extract_feature_importances(fitted_pipeline)
    assert isinstance(imp_df, pd.DataFrame)
    assert 'Feature' in imp_df.columns
    assert 'Importance' in imp_df.columns
    assert len(imp_df) == 30


def test_train_random_forest(sample_dataset):
    """Verify Random Forest fits on sample data, predicts valid probabilities, and yields feature importances."""
    X, y = sample_dataset
    pipeline = build_random_forest_pipeline(n_estimators=10, max_depth=5, random_state=42, n_jobs=-1)
    fitted_pipeline = train_tree_model(pipeline, X, y)
    
    preds = fitted_pipeline.predict(X)
    probas = fitted_pipeline.predict_proba(X)
    
    assert len(preds) == len(X)
    assert probas.shape == (len(X), 2)
    assert np.all(probas >= 0.0) and np.all(probas <= 1.0)
    
    eval_results = evaluate_model(fitted_pipeline, X, y, model_name="Random Forest Test")
    assert 'pr_auc' in eval_results
    assert 'roc_auc' in eval_results
    
    imp_df = extract_feature_importances(fitted_pipeline)
    assert isinstance(imp_df, pd.DataFrame)
    assert len(imp_df) == 30
