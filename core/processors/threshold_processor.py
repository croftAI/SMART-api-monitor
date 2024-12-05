from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import numpy as np
from datetime import datetime, timedelta
from collections import deque
import pandas as pd
from scipy import stats


@dataclass
class MetricWindow:
    window_size: timedelta
    data: deque
    timestamp: deque

    def __init__(self, window_size: timedelta):
        self.window_size = window_size
        self.data = deque()
        self.timestamp = deque()

    def add_point(self, value: float, timestamp: datetime):
        self.data.append(value)
        self.timestamp.append(timestamp)

        # Remove old data points
        while (timestamp - self.timestamp[0]) > self.window_size:
            self.data.popleft()
            self.timestamp.popleft()

    def get_statistics(self) -> Dict[str, float]:
        data_array = np.array(self.data)
        return {
            'mean': np.mean(data_array),
            'std': np.std(data_array),
            'median': np.median(data_array),
            'p95': np.percentile(data_array, 95),
            'p99': np.percentile(data_array, 99)
        }


class AdaptiveThresholdManager:
    def __init__(self, metric_name: str):
        self.metric_name = metric_name
        self.short_window = MetricWindow(timedelta(minutes=30))
        self.long_window = MetricWindow(timedelta(hours=24))
        self.baseline_stats: Optional[Dict[str, float]] = None
        self.current_threshold: float = 0
        self.adjustment_history: List[Tuple[datetime, float, str]] = []

    def add_metric(self, value: float, timestamp: datetime):
        """Add new metric value to both windows"""
        self.short_window.add_point(value, timestamp)
        self.long_window.add_point(value, timestamp)

    def calculate_adaptive_threshold(self) -> float:
        """Calculate new threshold based on recent and historical data"""
        short_stats = self.short_window.get_statistics()
        long_stats = self.long_window.get_statistics()

        # Calculate dynamic components
        recent_volatility = short_stats['std'] / short_stats['mean']
        historical_volatility = long_stats['std'] / long_stats['mean']

        # Adjust threshold based on volatility comparison
        if recent_volatility > historical_volatility * 1.5:
            # High volatility period - use more conservative threshold
            new_threshold = long_stats['p99']
        else:
            # Normal volatility - use dynamic threshold
            new_threshold = long_stats['p95'] + (short_stats['std'] * 2)

        return new_threshold

    def should_update_threshold(self, new_threshold: float) -> bool:
        """Determine if threshold should be updated"""
        if not self.current_threshold:
            return True

        threshold_change = abs(new_threshold - self.current_threshold) / self.current_threshold
        return threshold_change > 0.1  # 10% change threshold

    def update_threshold(self) -> Optional[float]:
        """Update threshold if necessary"""
        new_threshold = self.calculate_adaptive_threshold()

        if self.should_update_threshold(new_threshold):
            self.adjustment_history.append((
                datetime.now(),
                new_threshold,
                f"Updated from {self.current_threshold:.2f} to {new_threshold:.2f}"
            ))
            self.current_threshold = new_threshold
            return new_threshold
        return None


class StreamProcessor:
    def __init__(self):
        self.threshold_managers: Dict[str, AdaptiveThresholdManager] = {}
        self.alert_feedback: Dict[str, List[bool]] = {}  # Store alert accuracy feedback

    def process_metric(self, metric_name: str, value: float, timestamp: datetime):
        """Process incoming metric"""
        if metric_name not in self.threshold_managers:
            self.threshold_managers[metric_name] = AdaptiveThresholdManager(metric_name)

        manager = self.threshold_managers[metric_name]
        manager.add_metric(value, timestamp)

        # Check for threshold updates periodically
        if self._should_check_threshold(metric_name):
            new_threshold = manager.update_threshold()
            if new_threshold:
                self._handle_threshold_update(metric_name, new_threshold)

    def _should_check_threshold(self, metric_name: str) -> bool:
        """Determine if we should check for threshold updates"""
        # Implementation could consider:
        # - Time since last check
        # - Number of new data points
        # - System load
        # - Alert frequency
        return True  # Simplified for example

    def _handle_threshold_update(self, metric_name: str, new_threshold: float):
        """Handle threshold update"""
        # Update alert rules
        # Notify interested parties
        # Log change
        pass

    def add_alert_feedback(self, metric_name: str, was_useful: bool):
        """Add feedback about alert usefulness"""
        if metric_name not in self.alert_feedback:
            self.alert_feedback[metric_name] = []
        self.alert_feedback[metric_name].append(was_useful)

        # Adjust threshold sensitivity based on feedback
        if len(self.alert_feedback[metric_name]) >= 10:
            self._adjust_threshold_sensitivity(metric_name)

    def _adjust_threshold_sensitivity(self, metric_name: str):
        """Adjust threshold sensitivity based on alert feedback"""
        recent_feedback = self.alert_feedback[metric_name][-10:]
        false_positive_rate = 1 - (sum(recent_feedback) / len(recent_feedback))

        manager = self.threshold_managers[metric_name]
        if false_positive_rate > 0.2:  # Too many false positives
            # Make threshold less sensitive
            manager.current_threshold *= 1.1
        elif false_positive_rate < 0.05:  # Too few alerts
            # Make threshold more sensitive
            manager.current_threshold *= 0.9


class RealTimeMonitor:
    def __init__(self):
        self.stream_processor = StreamProcessor()
        self.metric_buffers: Dict[str, List[Tuple[datetime, float]]] = {}

    def process_log_entry(self, log_data: Dict):
        """Process incoming log entry"""
        timestamp = datetime.fromtimestamp(log_data['timestamp'])
        metrics = self._extract_metrics(log_data)

        for metric_name, value in metrics.items():
            self.stream_processor.process_metric(metric_name, value, timestamp)
            self._buffer_metric(metric_name, timestamp, value)

    def _extract_metrics(self, log_data: Dict) -> Dict[str, float]:
        """Extract metrics from log data"""
        # Implementation would depend on log format
        return {
            'response_time': float(log_data.get('response_time', 0)),
            'error_rate': float(log_data.get('error_rate', 0)),
            'event_count': float(log_data.get('event_count', 0))
        }

    def _buffer_metric(self, metric_name: str, timestamp: datetime, value: float):
        """Buffer metrics for batch processing"""
        if metric_name not in self.metric_buffers:
            self.metric_buffers[metric_name] = []
        self.metric_buffers[metric_name].append((timestamp, value))

        # Process buffer if enough data accumulated
        if len(self.metric_buffers[metric_name]) >= 100:
            self._process_metric_buffer(metric_name)

    def _process_metric_buffer(self, metric_name: str):
        """Process accumulated metrics"""
        buffer = self.metric_buffers[metric_name]
        df = pd.DataFrame(buffer, columns=['timestamp', 'value'])

        # Perform batch analysis
        # - Check for trends
        # - Detect seasonal patterns
        # - Update baseline statistics

        # Clear buffer
        self.metric_buffers[metric_name] = []


# Example usage
monitor = RealTimeMonitor()

# Simulate incoming log entries
sample_log = {
    'timestamp': datetime.now().timestamp(),
    'response_time': 150.0,
    'error_rate': 0.02,
    'event_count': 100
}

monitor.process_log_entry(sample_log)