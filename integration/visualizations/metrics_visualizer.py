import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List


class MetricsVisualizer:
    def create_time_series(self, data: pd.DataFrame, metric: str) -> go.Figure:
        fig = px.line(
            data,
            x='timestamp',
            y=metric,
            title=f'{metric} Over Time'
        )
        return fig

    def create_heatmap(self, data: pd.DataFrame) -> go.Figure:
        fig = go.Figure(data=go.Heatmap(
            z=data.values,
            x=data.columns,
            y=data.index,
            colorscale='Viridis'
        ))
        return fig

    def create_health_dashboard(self, health_data: Dict) -> List[go.Figure]:
        figures = []

        # Health Score Trend
        health_df = pd.DataFrame(health_data['health_scores'])
        figures.append(self.create_time_series(health_df, 'health_score'))

        # Component Scores
        comp_df = pd.DataFrame(health_data['component_scores'])
        figures.append(px.bar(comp_df, x='component', y='score'))

        return figures