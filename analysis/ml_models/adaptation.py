# analysis/ml_models/adaptation.py
from .validators import ModelValidator
from .performance_monitor import PerformanceMonitor
from .registry import ModelRegistry
from .orchestrator import MLModelOrchestrator


class AdaptationSystem:
    def __init__(self, config: Dict):
        self.validator = ModelValidator(config['validation'])
        self.performance_monitor = PerformanceMonitor()
        self.registry = ModelRegistry()
        self.orchestrator = MLModelOrchestrator()

    async def adapt_models(self):
        """Coordinate model adaptation process."""
        # Get current performance metrics
        performance = self.performance_monitor.get_current_metrics()

        # Check if adaptation is needed
        if self.should_adapt(performance):
            # Get new model candidates
            candidates = self.orchestrator.get_model_candidates()

            # Validate candidates
            valid_models = await self.validator.validate_models(candidates)

            # Register and deploy valid models
            for model in valid_models:
                self.registry.register_model(model)
                await self.orchestrator.deploy_model(model)

    def should_adapt(self, performance: Dict) -> bool:
        """Determine if adaptation is needed."""
        return (
                performance.accuracy_declining or
                performance.false_positives_increasing or
                self._time_since_last_adaptation.hours > 24
        )