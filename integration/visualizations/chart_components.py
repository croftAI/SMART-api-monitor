import plotly.graph_objects as go
from typing import Dict, List

class ChartComponents:
   @staticmethod
   def add_threshold_line(fig: go.Figure, threshold: float, name: str = 'Threshold'):
       fig.add_hline(
           y=threshold,
           line_dash="dash",
           line_color="red",
           annotation_text=name
       )
       return fig

   @staticmethod
   def add_annotations(fig: go.Figure, annotations: List[Dict]):
       for ann in annotations:
           fig.add_annotation(
               x=ann['x'],
               y=ann['y'],
               text=ann['text'],
               showarrow=True,
               arrowhead=1
           )
       return fig

   @staticmethod
   def create_gauge_chart(
       value: float,
       title: str,
       min_val: float = 0,
       max_val: float = 100
   ) -> go.Figure:
       return go.Figure(go.Indicator(
           mode = "gauge+number",
           value = value,
           title = {'text': title},
           gauge = {
               'axis': {'range': [min_val, max_val]},
               'threshold': {
                   'line': {'color': "red", 'width': 4},
                   'thickness': 0.75,
                   'value': 70
               }
           }
       ))