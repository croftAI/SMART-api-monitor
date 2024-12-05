from .context import APIContext


class HealthScoreCalculator:
    """Calculates comprehensive API health scores"""

    def __init__(self, context: APIContext):
        self.context = context
        self.weights = {
            'latency': 0.4,
            'error_rate': 0.3,
            'traffic': 0.3
        }

    # ... rest of the HealthScoreCalculator class methods