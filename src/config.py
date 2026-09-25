"""
Configuration module for Fraud Detection System.

Stores project-wide configuration constants including decision thresholds.
"""

# Default probability threshold used by standard classifiers
DEFAULT_THRESHOLD: float = 0.50

# Optimal probability threshold selected during Phase 6 threshold optimization
# Maximizes F1-score (0.8046) while maintaining 88.61% Precision and 73.68% Recall.
OPTIMAL_THRESHOLD: float = 0.70
