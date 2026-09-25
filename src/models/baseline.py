"""
Baseline Model Pipeline Module for Fraud Detection System.

Builds scikit-learn Pipelines pairing FraudDataPreprocessor with LogisticRegression.
"""

from typing import Optional, Union, Dict, Any
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from src.data.preprocessing import FraudDataPreprocessor


def build_baseline_pipeline(
    class_weight: Optional[Union[str, Dict[int, float]]] = None,
    solver: str = 'lbfgs',
    max_iter: int = 1000,
    random_state: int = 42
) -> Pipeline:
    """
    Creates a scikit-learn Pipeline incorporating RobustScaler preprocessing
    and Logistic Regression.

    Args:
        class_weight: Weight handling option for class imbalance ('balanced' or None).
        solver: Optimization algorithm for LogisticRegression (default: 'lbfgs').
        max_iter: Maximum solver convergence iterations (default: 1000).
        random_state: Seed for reproducibility.

    Returns:
        Configured scikit-learn Pipeline object.
    """
    preprocessor = FraudDataPreprocessor(scale_cols=['Time', 'Amount'])
    classifier = LogisticRegression(
        class_weight=class_weight,
        solver=solver,
        max_iter=max_iter,
        random_state=random_state
    )

    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', classifier)
    ])

    return pipeline


def train_baseline_model(
    X_train,
    y_train,
    class_weight: Optional[Union[str, Dict[int, float]]] = None,
    solver: str = 'lbfgs',
    max_iter: int = 1000,
    random_state: int = 42
) -> Pipeline:
    """
    Builds and fits a baseline Logistic Regression pipeline on training data.

    Returns:
        Fitted Pipeline object.
    """
    pipeline = build_baseline_pipeline(
        class_weight=class_weight,
        solver=solver,
        max_iter=max_iter,
        random_state=random_state
    )
    pipeline.fit(X_train, y_train)
    return pipeline
