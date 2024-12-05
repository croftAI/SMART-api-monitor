from .registry import ModelRegistry
import numpy as np


class ModelPerformanceMonitor:
    def __init__(self, model_registry: ModelRegistry):
        self.registry = model_registry
        self.performance_history = {}

    def update_model_performance(self, model_name: str, actual: float, predicted: float):
        error = abs(actual - predicted) / actual
        self.registry.update_performance(model_name, error)

        if self._should_retrain(model_name):
            self._trigger_model_retraining(model_name)

    def _should_retrain(self, model_name: str) -> bool:
        recent_performance = self.registry.model_performance[model_name][-10:]
        avg_error = np.mean(recent_performance)
        return avg_error > 0.2