# api/schemas/context_schemas.py

from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime

class APIContext(BaseModel):
    """Model for API context information."""
    api_name: str
    business_impact: float = Field(..., ge=0, le=1)
    criticality: float = Field(..., ge=0, le=1)
    dependencies: List[str]
    user_base: int
    peak_hours: List[int]
    maintenance_windows: Optional[List[Dict]]

class ContextUpdate(BaseModel):
    """Model for context update requests."""
    business_impact: Optional[float] = Field(None, ge=0, le=1)
    criticality: Optional[float] = Field(None, ge=0, le=1)
    dependencies: Optional[List[str]]
    user_base: Optional[int]
    peak_hours: Optional[List[int]]
    maintenance_windows: Optional[List[Dict]]

class DependencyInfo(BaseModel):
    """Model for API dependency information."""
    source: str
    target: str
    criticality: float = Field(..., ge=0, le=1)
    latency_impact: float
    error_rate: float = Field(..., ge=0, le=1)
    last_updated: datetime

class ContextResponse(BaseModel):
    """Response model for context queries."""
    api_name: str
    timestamp: datetime
    context: APIContext
    dependencies: List[DependencyInfo]
    health_impact_factor: float = Field(..., ge=0, le=1)