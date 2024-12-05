from typing import Dict
from datetime import datetime
from ..models.context import APIContext
from ..models.threshold_model import AdaptiveThreshold
from ..models.spike_model import SpikeDetector
from ..models.health_model import HealthScoreCalculator


class MonitoringSystem:
    """Main monitoring system that combines all components"""

    def __init__(self):
        self.apis: Dict[str, APIContext] = {}
        self.thresholds: Dict[str, AdaptiveThreshold] = {}
        self.spike_detectors: Dict[str, SpikeDetector] = {}
        self.health_calculators: Dict[str, HealthScoreCalculator] = {}

    # ... rest of the MonitoringSystem class methods