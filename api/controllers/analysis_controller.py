# api/controllers/analysis_controller.py

from typing import Dict, Optional
from datetime import datetime
from fastapi import HTTPException
from analysis.ml_models.orchestrator import MLModelOrchestrator
from analysis.context.context_collector import ContextCollector


class AnalysisController:
    """Controller for analysis-related operations."""

    def __init__(self):
        self.ml_orchestrator = MLModelOrchestrator()
        self.context_collector = ContextCollector()

    async def analyze_metrics(self, api_name: str, metrics: Dict) -> Dict:
        """Analyze metrics using ML models."""
        try:
            # Get context
            context = await self.context_collector.collect_context(
                api_name,
                datetime.now()
            )

            # Get ML insights
            insights = await self.ml_orchestrator.analyze_metrics(
                api_name,
                metrics,
                context
            )

            return {
                'analysis_id': insights['analysis_id'],
                'timestamp': datetime.now().isoformat(),
                'results': insights['results'],
                'recommendations': insights['recommendations']
            }
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Analysis failed: {str(e)}"
            )

    async def get_historical_analysis(
            self,
            api_name: str,
            start_time: datetime,
            end_time: datetime
    ) -> Dict:
        """Get historical analysis results."""
        try:
            return await self.ml_orchestrator.get_historical_analysis(
                api_name,
                start_time,
                end_time
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Historical analysis failed: {str(e)}"
            )