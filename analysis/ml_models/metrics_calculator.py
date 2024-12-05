# analysis/ml_models/metrics_calculator.py

from typing import Dict, List
import numpy as np
from scipy import stats
from datetime import datetime, timedelta


class ValidationMetricsCalculator:
    def __init__(self, config: Dict):
        self.config = config
        self.baseline_metrics = {}
        self.current_metrics = {}

    def calculate_validation_metrics(
            self,
            predictions: List[float],
            actuals: List[float],
            timestamps: List[datetime]
    ) -> Dict:
        """Calculate comprehensive validation metrics."""
        return {
            'accuracy': self._calculate_accuracy(predictions, actuals),
            'precision': self._calculate_precision(predictions, actuals),
            'recall': self._calculate_recall(predictions, actuals),
            'stability': self._calculate_stability(predictions, timestamps),
            'drift': self._calculate_drift(predictions, actuals),
            'confidence': self._calculate_confidence(predictions)
        }

    def _calculate_accuracy(self, predictions: List[float],
                            actuals: List[float]) -> float:
        """Calculate prediction accuracy."""
        correct = sum(1 for p, a in zip(predictions, actuals)
                      if abs(p - a) <= self.config['max_deviation'])
        return correct / len(predictions) if predictions else 0

    def _calculate_stability(self, predictions: List[float],
                             timestamps: List[datetime]) -> float:
        """Calculate prediction stability over time."""
        if len(predictions) < 2:
            return 0.0

        # Calculate variation over time windows
        window_size = timedelta(hours=1)
        windows = self._group_by_window(predictions, timestamps, window_size)

        variations = []
        for window_predictions in windows.values():
            if len(window_predictions) >= 2:
                variations.append(np.std(window_predictions))

        return 1.0 - (np.mean(variations) if variations else 0.0)

    def _calculate_drift(self, predictions: List[float],
                         actuals: List[float]) -> float:
        """Calculate concept drift between predictions and actuals."""
        if len(predictions) < self.config['min_samples']:
            return 0.0

        # Use Kolmogorov-Smirnov test to detect distribution drift
        ks_statistic, p_value = stats.ks_2samp(predictions, actuals)
        return ks_statistic

    def _calculate_confidence(self, predictions: List[float]) -> float:
        """Calculate prediction confidence scores."""
        if not predictions:
            return 0.0

        # Calculate confidence based on prediction variance
        prediction_std = np.std(predictions)
        prediction_mean = np.mean(predictions)

        # Normalize confidence score
        return 1.0 - min(prediction_std / prediction_mean
                         if prediction_mean != 0 else 1.0, 1.0)

    def _group_by_window(self, values: List[float],
                         timestamps: List[datetime],
                         window_size: timedelta) -> Dict:
        """Group values by time windows."""
        windows = {}
        for value, timestamp in zip(values, timestamps):
            window_start = timestamp.replace(
                minute=0, second=0, microsecond=0
            )
            if window_start not in windows:
                windows[window_start] = []
            windows[window_start].append(value)
        return windows