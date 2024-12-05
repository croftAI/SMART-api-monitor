# analysis/ml_models/seasonality_analyzer.py

from typing import Dict, List, Optional
import numpy as np
from scipy import signal
from datetime import datetime, timedelta
import pandas as pd


class SeasonalityAnalyzer:
    def __init__(self, config: Dict):
        self.config = config
        self.patterns = {}
        self.current_analysis = {}

    async def analyze_seasonality(
            self,
            values: List[float],
            timestamps: List[datetime]
    ) -> Dict:
        """Analyze time series for seasonal patterns."""
        df = pd.DataFrame({
            'value': values,
            'timestamp': timestamps
        }).set_index('timestamp')

        patterns = {
            'hourly': self._detect_hourly_pattern(df),
            'daily': self._detect_daily_pattern(df),
            'weekly': self._detect_weekly_pattern(df)
        }

        # Calculate confidence scores
        confidences = self._calculate_pattern_confidence(patterns, df)

        # Store significant patterns
        self.patterns = {
            period: pattern
            for period, pattern in patterns.items()
            if confidences[period] >= self.config['min_pattern_confidence']
        }

        return {
            'patterns': self.patterns,
            'confidences': confidences,
            'adjustments': self._calculate_adjustments(df)
        }

    def _detect_hourly_pattern(self, df: pd.DataFrame) -> Dict:
        """Detect hourly patterns in the data."""
        hourly_groups = df.groupby(df.index.hour)['value'].agg(['mean', 'std'])

        return {
            'means': hourly_groups['mean'].to_dict(),
            'stds': hourly_groups['std'].to_dict(),
            'peak_hour': hourly_groups['mean'].idxmax(),
            'trough_hour': hourly_groups['mean'].idxmin()
        }

    def _detect_daily_pattern(self, df: pd.DataFrame) -> Dict:
        """Detect daily patterns in the data."""
        daily_groups = df.groupby(df.index.day_name())['value'].agg(['mean', 'std'])

        return {
            'means': daily_groups['mean'].to_dict(),
            'stds': daily_groups['std'].to_dict(),
            'peak_day': daily_groups['mean'].idxmax(),
            'trough_day': daily_groups['mean'].idxmin()
        }

    def _detect_weekly_pattern(self, df: pd.DataFrame) -> Dict:
        """Detect weekly patterns in the data."""
        # Calculate weekly averages
        df['week'] = df.index.isocalendar().week
        weekly_pattern = df.groupby('week')['value'].agg(['mean', 'std'])

        # Detect repetitive patterns
        values = weekly_pattern['mean'].values
        if len(values) >= 2:
            # Use autocorrelation to detect patterns
            autocorr = signal.correlate(values, values, mode='full')
            return {
                'strength': float(np.max(autocorr[len(values):]) / autocorr[len(values) - 1]),
                'period': int(np.argmax(autocorr[len(values):]) + 1)
            }
        return {'strength': 0.0, 'period': 0}

    def _calculate_pattern_confidence(
            self,
            patterns: Dict,
            df: pd.DataFrame
    ) -> Dict[str, float]:
        """Calculate confidence scores for detected patterns."""
        confidences = {}

        for period, pattern in patterns.items():
            if period in ['hourly', 'daily']:
                # Calculate coefficient of variation
                means = np.array(list(pattern['means'].values()))
                stds = np.array(list(pattern['stds'].values()))
                cv = np.mean(stds) / np.mean(means) if np.mean(means) != 0 else 0
                confidences[period] = 1.0 - min(cv, 1.0)
            else:  # weekly
                confidences[period] = pattern['strength']

        return confidences

    def _calculate_adjustments(self, df: pd.DataFrame) -> Dict:
        """Calculate adjustment factors based on patterns."""
        adjustments = {}

        # Current time components
        current_hour = datetime.now().hour
        current_day = datetime.now().strftime('%A')
        current_week = datetime.now().isocalendar()[1]

        # Apply pattern-based adjustments
        for period, pattern in self.patterns.items():
            if period == 'hourly' and current_hour in pattern['means']:
                adjustments['hourly'] = (
                        pattern['means'][current_hour] /
                        np.mean(list(pattern['means'].values()))
                )
            elif period == 'daily' and current_day in pattern['means']:
                adjustments['daily'] = (
                        pattern['means'][current_day] /
                        np.mean(list(pattern['means'].values()))
                )

        return adjustments

    def get_current_adjustment(self) -> float:
        """Get the current combined adjustment factor."""
        if not self.patterns:
            return 1.0

        adjustments = self._calculate_adjustments(None)  # Current time only
        return np.prod(list(adjustments.values()))