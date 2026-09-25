"""
Nonlinear Tree-Based Models Module for Fraud Detection System.

Builds scikit-learn Pipelines pairing FraudDataPreprocessor with DecisionTreeClassifier
and RandomForestClassifier.
"""

from typing import Optional, Union, Dict, Any, List
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from src.data.preprocessing import FraudDataPreprocessor


def build_decision_tree_pipeline(
    class_weight: Optional[Union[str, Dict[int, float]]] = 'balanced',
    max_depth: Optional[int] = 10,
    min_samples_split: int = 10,
    random_state: int = 42
) -> Pipeline:
    """
    Creates a scikit-learn Pipeline incorporating RobustScaler preprocessing
    and DecisionTreeClassifier.

    Args:
        class_weight: Weight handling option ('balanced', None, or custom dict).
        max_depth: Maximum tree depth to control overfitting (default: 10).
        min_samples_split: Minimum samples required to split an internal node (default: 10).
        random_state: Seed for reproducibility.

    Returns:
        Configured Pipeline object.
    """
    preprocessor = FraudDataPreprocessor(scale_cols=['Time', 'Amount'])
    classifier = DecisionTreeClassifier(
        class_weight=class_weight,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        random_state=random_state
    )

    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', classifier)
    ])

    return pipeline


def build_random_forest_pipeline(
    n_estimators: int = 100,
    class_weight: Optional[Union[str, Dict[int, float]]] = 'balanced',
    max_depth: Optional[int] = 10,
    min_samples_split: int = 10,
    random_state: int = 42,
    n_jobs: int = -1
) -> Pipeline:
    """
    Creates a scikit-learn Pipeline incorporating RobustScaler preprocessing
    and RandomForestClassifier.

    Args:
        n_estimators: Number of trees in the forest (default: 100).
        class_weight: Weight handling option ('balanced', 'balanced_subsample', None).
        max_depth: Maximum tree depth (default: 10).
        min_samples_split: Minimum samples required to split node (default: 10).
        random_state: Seed for reproducibility.
        n_jobs: Number of parallel CPU jobs (-1 for all processors).

    Returns:
        Configured Pipeline object.
    """
    preprocessor = FraudDataPreprocessor(scale_cols=['Time', 'Amount'])
    classifier = RandomForestClassifier(
        n_estimators=n_estimators,
        class_weight=class_weight,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        random_state=random_state,
        n_jobs=n_jobs
    )

    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', classifier)
    ])

    return pipeline


def train_tree_model(
    pipeline: Pipeline,
    X_train: pd.DataFrame,
    y_train: pd.Series
) -> Pipeline:
    """
    Fits a tree pipeline on training data.

    Returns:
        Fitted Pipeline object.
    """
    pipeline.fit(X_train, y_train)
    return pipeline


def extract_feature_importances(pipeline: Pipeline) -> pd.DataFrame:
    """
    Extracts feature importance scores from a fitted tree-based pipeline.

    Returns:
        pandas DataFrame sorted by feature importance descending.
    """
    preprocessor = pipeline.named_steps['preprocessor']
    classifier = pipeline.named_steps['classifier']

    if not hasattr(classifier, 'feature_importances_'):
        raise AttributeError(f"Classifier {type(classifier).__name__} does not support feature_importances_.")

    feature_names = preprocessor.feature_names_out_
    importances = classifier.feature_importances_

    df_imp = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importances
    }).sort_values(by='Importance', ascending=False).reset_index(drop=True)

    return df_imp
