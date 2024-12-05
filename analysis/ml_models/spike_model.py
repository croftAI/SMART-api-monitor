from collections import deque
import numpy as np


class SpikeDetector:
    """Detects and analyzes traffic spikes"""

    def __init__(self, window_size: int = 30):
        self.window = deque(maxlen=window_size)
        self.baseline = None
        self.threshold_multiplier = 2.0

    # ... rest of the SpikeDetector class methods