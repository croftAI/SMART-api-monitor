from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, List
from ..schemas.monitoring_schemas import (
    MetricData,
    ThresholdConfig,
    AnalysisResponse
)
from ..controllers.monitoring_controller import MonitoringController
from ..middleware.auth_middleware import verify_api_key

router = APIRouter(prefix="/v1/monitoring", tags=["monitoring"])
controller = MonitoringController()

@router.post("/metrics", response_model=AnalysisResponse)
async def process_metrics(
    metric_data: MetricData,
    api_key: str = Depends(verify_api_key)
):
    """Process new metric data and return analysis."""
    try:
        return await controller.process_metrics(metric_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health/{api_name}")
async def get_health(
    api_name: str,
    api_key: str = Depends(verify_api_key)
):
    """Get current health status for an API."""
    try:
        return await controller.get_api_health(api_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/thresholds/{api_name}")
async def update_thresholds(
    api_name: str,
    config: ThresholdConfig,
    api_key: str = Depends(verify_api_key)
):
    """Update threshold configuration for an API."""
    try:
        return await controller.update_thresholds(api_name, config)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))