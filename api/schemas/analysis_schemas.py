# api/schemas/analysis_schemas.py

from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime

class MetricAnalysisRequest(BaseModel):
    """Request model for metric analysis."""
    api_name: str = Field(..., description="Name of the API to analyze")
    metrics: Dict[str, float] = Field(..., description="Metric values to analyze")
    timestamp: datetime = Field(default_factory=datetime.now)
    context: Optional[Dict] = Field(default=None, description="Additional context")

class AnalysisResult(BaseModel):
    """Response model for analysis results."""
    analysis_id: str
    timestamp: datetime
    api_name: str
    anomalies: List[Dict]
    insights: Dict
    recommendations: List[str]
    confidence_score: float = Field(..., ge=0, le=1)

class HistoricalAnalysisRequest(BaseModel):
    """Request model for historical analysis."""
    start_time: datetime
    end_time: datetime
    metrics: List[str] = Field(default=["all"])
    aggregation: Optional[str] = Field(default="hour")

class TrendAnalysisResponse(BaseModel):
    """Response model for trend analysis."""
    api_name: str
    period: str
    trends: Dict[str, Dict]
    correlations: Dict[str, float]
    seasonal_patterns: Optional[Dict]
    confidence: float = Field(..., ge=0, le=1)