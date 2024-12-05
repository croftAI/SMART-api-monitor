from typing import Dict, List
from datetime import datetime


class ModelRegistry:
    def __init__(self):
        self.models: Dict[str, Dict] = {}
        self.model_performance: Dict[str, List[float]] = {}

    def register_model(self, model_name: str, model_type: str, model_instance: any):
        self.models[model_name] = {
            'type': model_type,
            'instance': model_instance,
            'created_at': datetime.now(),
            'last_updated': datetime.now()
        }

    def update_performance(self, model_name: str, performance_metric: float):
        if model_name not in self.model_performance:
            self.model_performance[model_name] = []
        self.model_performance[model_name].append(performance_metric)