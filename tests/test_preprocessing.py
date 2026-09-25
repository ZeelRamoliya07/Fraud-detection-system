"""
Unit and Integration Tests for Data Preprocessing Module.
"""

import pytest
import pandas as pd
import numpy as np
from src.data.preprocessing import (
    validate_data,
    analyze_duplicates,
    split_features_target,
    perform_train_test_split,
    FraudDataPreprocessor,
    process_raw_data
)


@pytest.fixture
def sample_raw_data() -> pd.DataFrame:
    """Creates a synthetic dummy dataset matching Credit Card Fraud dataset schema."""
    np.random.seed(42)
    n_samples = 100
    
    data = {
        'Time': np.random.uniform(0, 100000, n_samples),
        'Amount': np.random.exponential(scale=50, size=n_samples),
    }
    
    # Add V1 through V28
    for i in range(1, 29):
        data[f'V{i}'] = np.random.normal(0, 1, n_samples)
        
    # Add target Class (90 legitimate, 10 fraud)
    data['Class'] = np.array([0] * 90 + [1] * 10)
    
    df = pd.DataFrame(data)
    return df


def test_validate_data_valid(sample_raw_data):
    """Test data validation passes with valid schema."""
    # Should not raise any exception
    validate_data(sample_raw_data, target_col='Class')


def test_validate_data_missing_target(sample_raw_data):
    """Test validation fails when target column is missing."""
    df_no_target = sample_raw_data.drop(columns=['Class'])
    with pytest.raises(ValueError, match="Target column 'Class' not found"):
        validate_data(df_no_target, target_col='Class')


def test_validate_data_invalid_target_values(sample_raw_data):
    """Test validation fails when target contains non-binary values."""
    df_invalid_target = sample_raw_data.copy()
    df_invalid_target.loc[0, 'Class'] = 99
    with pytest.raises(ValueError, match="contains invalid values"):
        validate_data(df_invalid_target, target_col='Class')


def test_validate_data_nulls(sample_raw_data):
    """Test validation fails when missing values are present."""
    df_nulls = sample_raw_data.copy()
    df_nulls.loc[0, 'Amount'] = np.nan
    with pytest.raises(ValueError, match="Unexpected missing values detected"):
        validate_data(df_nulls, target_col='Class')


def test_target_separation(sample_raw_data):
    """Test features X and target y are correctly separated without leakage."""
    X, y = split_features_target(sample_raw_data, target_col='Class')
    
    assert 'Class' not in X.columns, "Target column 'Class' leaked into feature set X."
    assert len(X.columns) == 30, f"Expected 30 features, got {len(X.columns)}"
    assert len(X) == len(sample_raw_data)
    assert len(y) == len(sample_raw_data)
    assert set(y.unique()) == {0, 1}


def test_train_test_split_stratified(sample_raw_data):
    """Test stratified split preserves class ratio and shapes."""
    X, y = split_features_target(sample_raw_data, target_col='Class')
    X_train, X_test, y_train, y_test = perform_train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    assert len(X_train) == 80
    assert len(X_test) == 20
    assert len(y_train) == 80
    assert len(y_test) == 20
    
    # Verify stratification
    assert y_train.value_counts()[1] == 8
    assert y_test.value_counts()[1] == 2


def test_fraud_data_preprocessor_fitting_and_transform(sample_raw_data):
    """Test FraudDataPreprocessor fits on train data and transforms unseen test data."""
    X, y = split_features_target(sample_raw_data, target_col='Class')
    X_train, X_test, y_train, y_test = perform_train_test_split(X, y, test_size=0.2, random_state=42)
    
    preprocessor = FraudDataPreprocessor(scale_cols=['Time', 'Amount'])
    X_train_scaled = preprocessor.fit_transform(X_train)
    X_test_scaled = preprocessor.transform(X_test)
    
    # Check shapes
    assert X_train_scaled.shape == (80, 30)
    assert X_test_scaled.shape == (20, 30)
    
    # Check feature names match
    assert list(X_train_scaled.columns) == list(X_test_scaled.columns)
    assert 'Time' in X_train_scaled.columns
    assert 'Amount' in X_train_scaled.columns
    assert 'Class' not in X_train_scaled.columns


def test_process_raw_data_end_to_end(sample_raw_data):
    """Test complete process_raw_data function."""
    result = process_raw_data(sample_raw_data, target_col='Class', remove_duplicates=False, test_size=0.2)
    
    assert 'X_train_scaled' in result
    assert 'X_test_scaled' in result
    assert 'y_train' in result
    assert 'y_test' in result
    assert 'preprocessor' in result
    assert result['X_train_scaled'].shape == (80, 30)
    assert result['X_test_scaled'].shape == (20, 30)
