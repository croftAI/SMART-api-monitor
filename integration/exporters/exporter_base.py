from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class MetricsExporter(ABC):
    @abstractmethod
    async def export_metrics(self, metrics: Dict):
        """Export metrics to external system."""
        pass

    @abstractmethod
    async def export_batch(self, metrics_batch: List[Dict]):
        """Export batch of metrics."""
        pass

    @abstractmethod
    async def check_connection(self) -> bool:
        """Check connection to export destination."""
        pass