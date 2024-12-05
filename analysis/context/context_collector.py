from typing import Dict, Optional
from datetime import datetime
from .business_impact import BusinessImpactAnalyzer
from .user_analysis import UserBehaviorAnalyzer
from ..predictive.seasonality import SeasonalityAnalyzer

class ContextCollector:
    def __init__(self):
        self.business_analyzer = BusinessImpactAnalyzer()
        self.user_analyzer = UserBehaviorAnalyzer()
        self.seasonality_analyzer = SeasonalityAnalyzer()

    def collect_context(self, api_name: str,
                       timestamp: datetime) -> Dict:
        """Collect all relevant context for decision making."""
        business_impact = self.business_analyzer.analyze_impact(
            api_name, self._get_recent_metrics(api_name)
        )
        user_patterns = self.user_analyzer.analyze_user_patterns(
            api_name, 'last_24h'
        )
        seasonal_factors = self.seasonality_analyzer.get_seasonal_adjustments(
            api_name, timestamp
        )

        return {
            'business_context': business_impact,
            'user_context': user_patterns,
            'seasonal_context': seasonal_factors,
            'collected_at': timestamp
        }

    def _get_recent_metrics(self, api_name: str) -> Dict:
        """Get recent metrics for an API."""
        pass