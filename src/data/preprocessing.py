"""
Data Preprocessing Module for Fraud Detection System.

Provides reusable data validation, duplicate analysis, train/test splitting,
and feature scaling pipelines while strictly preventing data leakage.
"""

from typing import Tuple, Dict, Any, List, Optional
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler
from sklearn.compose import ColumnTransformer
from sklearn.base import BaseEstimator, TransformerMixin


def validate_data(df: pd.DataFrame, target_col: str = 'Class') -> None:
    """
    Validates input DataFrame schema, target column existence, null values,
    data types, and target values.

    Raises:
        TypeError: If df is not a pandas DataFrame.
        ValueError: If df is empty, missing target column, contains nulls, non-numeric data,
                    or invalid target values.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Expected pandas DataFrame, got {type(df).__name__}")
    
    if df.empty:
        raise ValueError("Input DataFrame is empty.")
    
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found in DataFrame columns.")
    
    # Expected minimal feature set
    required_features = ['Time', 'Amount'] + [f'V{i}' for i in range(1, 29)]
    missing_features = [col for col in required_features if col not in df.columns]
    if missing_features:
        raise ValueError(f"Missing required dataset features: {missing_features}")

    # Check for missing values
    null_counts = df.isnull().sum()
    if null_counts.sum() > 0:
        cols_with_nulls = null_counts[null_counts > 0].to_dict()
        raise ValueError(f"Unexpected missing values detected: {cols_with_nulls}")
    
    # Check data types (all columns must be numeric)
    non_numeric_cols = [col for col in df.columns if not np.issubdtype(df[col].dtype, np.number)]
    if non_numeric_cols:
        raise ValueError(f"Non-numeric columns detected: {non_numeric_cols}")

    # Check target value binary integrity
    unique_targets = set(df[target_col].unique())
    if not unique_targets.issubset({0, 1}):
        raise ValueError(f"Target column '{target_col}' contains invalid values: {unique_targets}. Expected only {{0, 1}}.")


def analyze_duplicates(df: pd.DataFrame, target_col: str = 'Class') -> Dict[str, Any]:
    """
    Analyzes duplicate rows in the dataset and breaks down duplicates by target class.

    Returns:
        Dict containing total rows, total duplicates, duplicate percentage,
        and duplicate counts by target class.
    """
    validate_data(df, target_col=target_col)
    
    total_rows = len(df)
    duplicate_mask = df.duplicated()
    total_duplicates = int(duplicate_mask.sum())
    duplicate_pct = (total_duplicates / total_rows) * 100 if total_rows > 0 else 0.0

    dups_by_class = df[duplicate_mask][target_col].value_counts().to_dict()
    
    return {
        'total_rows': total_rows,
        'total_duplicates': total_duplicates,
        'duplicate_percentage': duplicate_pct,
        'class_0_duplicates': dups_by_class.get(0, 0),
        'class_1_duplicates': dups_by_class.get(1, 0)
    }


def split_features_target(df: pd.DataFrame, target_col: str = 'Class') -> Tuple[pd.DataFrame, pd.Series]:
    """
    Separates input feature set X from target label y.

    Returns:
        Tuple of (X, y) where X excludes target_col and y is target_col.
    """
    validate_data(df, target_col=target_col)
    X = df.drop(columns=[target_col]).copy()
    y = df[target_col].copy()
    return X, y


def perform_train_test_split(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float = 0.2,
    random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Performs stratified train/test split to preserve severe class imbalance.

    Returns:
        Tuple of (X_train, X_test, y_train, y_test)
    """
    if len(X) != len(y):
        raise ValueError(f"Features length ({len(X)}) does not match target length ({len(y)}).")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        stratify=y,
        random_state=random_state
    )
    return X_train, X_test, y_train, y_test


class FraudDataPreprocessor(BaseEstimator, TransformerMixin):
    """
    Scikit-Learn compatible transformer pipeline for scaling transaction features
    ('Time' and 'Amount') while leaving pre-scaled PCA features ('V1'..'V28') intact.
    
    Prevents data leakage by fitting scaling parameters strictly on training set.
    """
    
    def __init__(self, scale_cols: Optional[List[str]] = None):
        self.scale_cols = scale_cols if scale_cols is not None else ['Time', 'Amount']
        self.ct: Optional[ColumnTransformer] = None
        self.feature_names_out_: Optional[List[str]] = None

    def fit(self, X: pd.DataFrame, y: Optional[pd.Series] = None):
        """
        Fits RobustScaler on specified columns (Time, Amount) using training data ONLY.
        """
        passthrough_cols = [col for col in X.columns if col not in self.scale_cols]
        
        self.ct = ColumnTransformer(
            transformers=[
                ('scaler', RobustScaler(), self.scale_cols),
                ('passthrough', 'passthrough', passthrough_cols)
            ],
            remainder='drop'
        )
        self.ct.fit(X)
        self.feature_names_out_ = self.scale_cols + passthrough_cols
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Transforms features using learned scaling parameters.
        Returns scaled pandas DataFrame with matching feature column ordering.
        """
        if self.ct is None:
            raise RuntimeError("Preprocessor has not been fitted yet. Call fit() before transform().")

        transformed_array = self.ct.transform(X)
        return pd.DataFrame(transformed_array, columns=self.feature_names_out_, index=X.index)


def process_raw_data(
    df: pd.DataFrame,
    target_col: str = 'Class',
    remove_duplicates: bool = True,
    test_size: float = 0.2,
    random_state: int = 42
) -> Dict[str, Any]:
    """
    End-to-end preprocessing function:
    1. Validates data schema & integrity.
    2. Analyzes duplicates.
    3. Optionally removes duplicate records (prior to split).
    4. Separates X and y.
    5. Performs stratified train/test split.
    6. Fits FraudDataPreprocessor ONLY on training set (prevents leakage).
    7. Transforms train and test sets.

    Returns:
        Dict containing scaled data, unscaled data, preprocessor artifact, and stats.
    """
    validate_data(df, target_col=target_col)
    dup_stats = analyze_duplicates(df, target_col=target_col)
    
    working_df = df.copy()
    if remove_duplicates and dup_stats['total_duplicates'] > 0:
        working_df = working_df.drop_duplicates().reset_index(drop=True)

    X, y = split_features_target(working_df, target_col=target_col)
    X_train, X_test, y_train, y_test = perform_train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    preprocessor = FraudDataPreprocessor(scale_cols=['Time', 'Amount'])
    X_train_scaled = preprocessor.fit_transform(X_train)
    X_test_scaled = preprocessor.transform(X_test)

    return {
        'X_train_scaled': X_train_scaled,
        'X_test_scaled': X_test_scaled,
        'y_train': y_train,
        'y_test': y_test,
        'preprocessor': preprocessor,
        'duplicate_stats': dup_stats,
        'removed_duplicates': remove_duplicates
    }
