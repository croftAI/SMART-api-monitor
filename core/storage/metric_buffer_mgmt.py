from typing import Dict, List, Optional
from collections import deque
import numpy as np


class MetricBuffer:
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self.buffers: Dict[str, deque] = {}

    def add_metric(self, api_name: str, metric_type: str, value: float):
        """Add new metric to buffer."""
        buffer_key = f"{api_name}:{metric_type}"
        if buffer_key not in self.buffers:
            self.buffers[buffer_key] = deque(maxlen=self.max_size)

        self.buffers[buffer_key].append(value)

    def get_statistics(self, api_name: str,
                       metric_type: str) -> Dict[str, float]:
        """Get statistical summary of buffered metrics."""
        buffer_key = f"{api_name}:{metric_type}"
        if buffer_key not in self.buffers:
            return {}

        values = np.array(self.buffers[buffer_key])
        return {
            'mean': np.mean(values),
            'std': np.std(values),
            'min': np.min(values),
            'max': np.max(values),
            'p95': np.percentile(values, 95)
        }