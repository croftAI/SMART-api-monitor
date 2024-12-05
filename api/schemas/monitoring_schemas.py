from pydantic import BaseModel, Field
from typing import Dict, Optional, List
from datetime import datetime

class MetricData(BaseModel):
    api_name: str
    timestamp: datetime
    latency: float = Field(..., gt=0)
    error_rate: float = Field(..., ge=0, le=1)
    traffic: float = Field(..., ge=0)

class ThresholdConfig(BaseModel):
    window_size: int = Field(default=300, gt=0)
    sensitivity: float = Field(default=2.0, gt=0)
    min_data_points: int = Field(default=30, gt=0)

class AnalysisResponse(BaseModel):
    timestamp: datetime
    current_threshold: float
    is_spike: bool
    health_score: float
    status: str
    needs_attention: bool
    details: Optional[Dict] = None