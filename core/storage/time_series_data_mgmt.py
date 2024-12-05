from typing import Dict, List, Optional
from datetime import datetime, timedelta
import numpy as np


class TimeSeriesBuffer:
    def __init__(self, retention_period: timedelta = timedelta(hours=24)):
        self.retention_period = retention_period
        self.data: Dict[str, List[tuple]] = {}  # api_name -> [(timestamp, value)]

    def add_point(self, api_name: str, timestamp: datetime, value: float):
        """Add new data point to time series."""
        if api_name not in self.data:
            self.data[api_name] = []

        self.data[api_name].append((timestamp, value))
        self._cleanup_old_data(api_name)

    def get_range(self, api_name: str,
                  start_time: datetime,
                  end_time: datetime) -> List[tuple]:
        """Get time series data within specified range."""
        if api_name not in self.data:
            return []

        return [
            (ts, val) for ts, val in self.data[api_name]
            if start_time <= ts <= end_time
        ]

    def _cleanup_old_data(self, api_name: str):
        """Remove data points older than retention period."""
        cutoff_time = datetime.now() - self.retention_period
        self.data[api_name] = [
            (ts, val) for ts, val in self.data[api_name]
            if ts > cutoff_time
        ]