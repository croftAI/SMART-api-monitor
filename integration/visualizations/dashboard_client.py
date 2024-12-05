from typing import Dict, List, Optional
from datetime import datetime, timedelta
import pandas as pd


class DashboardClient:
    def __init__(self, config: Dict):
        self.config = config
        self.cache = {}

    async def get_metrics_data(
            self,
            api_name: str,
            metric_type: str,
            time_range: timedelta
    ) -> pd.DataFrame:
        """Fetch metrics data for visualization."""
        pass

    async def update_dashboard(self, new_data: Dict):
        """Update dashboard with new data."""
        pass

    def generate_chart_config(self, chart_type: str, data: Dict) -> Dict:
        """Generate configuration for different chart types."""
        pass