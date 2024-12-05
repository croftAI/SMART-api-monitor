from .registry import ModelRegistry
from .models.prophet_model import ProphetModel
from .models.isolation_forest_model import IsolationForestModel
from .models.lstm_model import LSTMModel
from .adaptation import AdaptationSystem


class MLModelOrchestrator:
    def __init__(self):
        self.registry = ModelRegistry()
        self.initialize_models()

    def initialize_models(self):
        # Initialize all models
        self.registry.register_model('prophet', 'forecasting', ProphetModel())
        self.registry.register_model('isolation_forest', 'anomaly_detection', IsolationForestModel())
        self.registry.register_model('lstm', 'sequence_prediction', LSTMModel())


class MLModelOrchestrator:
    def __init__(self):
        self.adaptation_system = AdaptationSystem(self.config)

    async def process_metrics(self, metrics: Dict):
        """Process metrics and potentially adapt."""
        # Normal processing
        results = await self._process_metrics(metrics)

        # Check for adaptation
        await self.adaptation_system.adapt_models()

        return results