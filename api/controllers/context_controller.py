# api/controllers/context_controller.py

from typing import Dict, Optional
from datetime import datetime
from fastapi import HTTPException
from analysis.context.context_collector import ContextCollector
from analysis.context.dependency_analyzer import DependencyAnalyzer


class ContextController:
    """Controller for context-related operations."""

    def __init__(self):
        self.context_collector = ContextCollector()
        self.dependency_analyzer = DependencyAnalyzer()

    async def get_api_context(self, api_name: str) -> Dict:
        """Get current context for an API."""
        try:
            context = await self.context_collector.collect_context(
                api_name,
                datetime.now()
            )

            # Enhance with dependency information
            dependencies = {
                'impact_score': self.dependency_analyzer.get_impact_score(api_name),
                'critical_path': self.dependency_analyzer.get_critical_path(api_name),
                'dependent_apis': self.dependency_analyzer.get_dependent_apis(api_name)
            }

            return {
                'api_name': api_name,
                'timestamp': datetime.now().isoformat(),
                'context': context,
                'dependencies': dependencies
            }
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Context collection failed: {str(e)}"
            )

    async def update_api_context(
            self,
            api_name: str,
            context_update: Dict
    ) -> Dict:
        """Update context for an API."""
        try:
            updated_context = await self.context_collector.update_context(
                api_name,
                context_update
            )
            return {
                'api_name': api_name,
                'timestamp': datetime.now().isoformat(),
                'updated_context': updated_context
            }
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Context update failed: {str(e)}"
            )