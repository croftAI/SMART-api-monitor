# api/routes/analysis_routes.py

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Optional
from datetime import datetime
from ..controllers.analysis_controller import AnalysisController
from ..middleware.auth_middleware import verify_api_key
from ..schemas.monitoring_schemas import MetricData, AnalysisResponse

router = APIRouter(prefix="/v1/analysis", tags=["analysis"])
controller = AnalysisController()

@router.post("/metrics/{api_name}", response_model=AnalysisResponse)
async def analyze_metrics(
    api_name: str,
    metric_data: MetricData,
    api_key: str = Depends(verify_api_key)
):
    """Analyze metrics for a specific API."""
    try:
        return await controller.analyze_metrics(api_name, metric_data.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{api_name}")
async def get_historical_analysis(
    api_name: str,
    start_time: datetime,
    end_time: datetime,
    api_key: str = Depends(verify_api_key)
):
    """Get historical analysis results."""
    try:
        return await controller.get_historical_analysis(
            api_name,
            start_time,
            end_time
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/trends/{api_name}")
async def get_trend_analysis(
    api_name: str,
    window_hours: Optional[int] = 24,
    api_key: str = Depends(verify_api_key)
):
    """Get trend analysis for an API."""
    try:
        return await controller.get_trend_analysis(
            api_name,
            window_hours
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))