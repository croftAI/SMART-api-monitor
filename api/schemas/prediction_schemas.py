# api/schemas/prediction_schemas.py

from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime

class ForecastRequest(BaseModel):
    """Request model for traffic forecasting."""
    horizon_hours: int = Field(..., gt=0, le=168)
    granularity: str = Field(default="hour")
    include_confidence: bool = Field(default=True)
    consider_seasonality: bool = Field(default=True)

class TrafficPrediction(BaseModel):
    """Model for traffic prediction results."""
    timestamp: datetime
    predicted_value: float
    confidence_lower: Optional[float]
    confidence_upper: Optional[float]
    seasonality_impact: Optional[float]

class ThresholdPrediction(BaseModel):
    """Model for threshold prediction results."""
    api_name: str
    timestamp: datetime
    predictions: List[Dict[str, float]]
    confidence_scores: Dict[str, float]
    factors: Dict[str, float]
    valid_until: datetime

class SeasonalPattern(BaseModel):
    """Model for seasonal pattern analysis."""
    pattern_type: str
    strength: float = Field(..., ge=0, le=1)
    cycle_length: str
    peak_times: List[str]
    trough_times: List[str]
    confidence: float = Field(..., ge=0, le=1)

class PredictionResponse(BaseModel):
    """Generic response model for predictions."""
    request_id: str
    timestamp: datetime
    api_name: str
    predictions: List[Dict]
    metadata: Dict
    model_version: str
    confidence_score: float = Field(..., ge=0, le=1)