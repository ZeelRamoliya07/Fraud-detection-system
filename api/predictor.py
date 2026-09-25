"""
Prediction Service Component for Fraud Detection System API.

Loads the serialized Random Forest pipeline artifact once upon initialization,
transforms input transaction features, and evaluates fraud probability against OPTIMAL_THRESHOLD.
"""

import os
from typing import Dict, Any, Optional
import pandas as pd
import joblib
from src.config import OPTIMAL_THRESHOLD

# Exact ordered feature list expected by the trained preprocessor & model
FEATURE_COLUMNS = ['Time'] + [f'V{i}' for i in range(1, 29)] + ['Amount']


class FraudPredictor:
    """
    Service component for managing model inference and classification risk scoring.
    """

    def __init__(self, model_path: Optional[str] = None, threshold: float = OPTIMAL_THRESHOLD):
        if model_path is None:
            # Resolve relative model path from current file or workspace root
            root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            model_path = os.path.join(root_dir, 'models', 'random_forest.joblib')

        self.model_path = model_path
        self.threshold = threshold
        self.pipeline = self._load_pipeline(model_path)

    def _load_pipeline(self, model_path: str) -> Any:
        """Loads serialized joblib model pipeline artifact."""
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Serialized model pipeline artifact not found at: {model_path}")
        try:
            pipeline = joblib.load(model_path)
            return pipeline
        except Exception as e:
            raise RuntimeError(f"Failed to load model pipeline artifact from '{model_path}': {str(e)}")

    @staticmethod
    def get_risk_level(probability: float) -> str:
        """
        Maps fraud probability to application-level risk level.
        
        Mapping:
          probability < 0.30          -> LOW
          0.30 <= probability < 0.70  -> MEDIUM
          probability >= 0.70         -> HIGH
        """
        if probability < 0.30:
            return "LOW"
        elif probability < 0.70:
            return "MEDIUM"
        else:
            return "HIGH"

    def predict(self, transaction_data: Dict[str, float]) -> Dict[str, Any]:
        """
        Executes prediction pipeline for a single transaction dictionary.

        Args:
            transaction_data: Dict containing all 30 feature values.

        Returns:
            Dict containing fraud_probability, is_fraud, risk_level, and threshold.
        """
        # Convert dictionary to DataFrame with exact column ordering
        df_input = pd.DataFrame([transaction_data], columns=FEATURE_COLUMNS)

        # Predict probability for positive class (Fraud = 1)
        proba = float(self.pipeline.predict_proba(df_input)[0, 1])

        # Evaluate binary classification against operational threshold (0.70)
        is_fraud = bool(proba >= self.threshold)
        risk_level = self.get_risk_level(proba)

        return {
            'fraud_probability': proba,
            'is_fraud': is_fraud,
            'risk_level': risk_level,
            'threshold': self.threshold
        }
