# api/routes/prediction_routes.py

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Optional
from ..controllers.prediction_controller import PredictionController
from ..middleware.auth_middleware import verify_api_key
from ..schemas.monitoring_schemas import ForecastRequest

router = APIRouter(prefix="/v1/prediction", tags=["prediction"])
controller = PredictionController()

@router.post("/traffic/{api_name}")
async def predict_traffic(
    api_name: str,
    forecast_request: ForecastRequest,
    api_key: str = Depends(verify_api_key)
):
    """Predict traffic patterns for an API."""
    try:
        return await controller.predict_traffic(
            api_name,
            forecast_request.horizon_hours
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/thresholds/{api_name}")
async def predict_thresholds(
    api_name: str,
    forecast_data: Dict,
    api_key: str = Depends(verify_api_key)
):
    """Predict optimal thresholds based on forecasted conditions."""
    try:
        return await controller.predict_thresholds(api_name, forecast_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/patterns/{api_name}")
async def get_seasonal_patterns(
    api_name: str,
    lookback_days: Optional[int] = 30,
    api_key: str = Depends(verify_api_key)
):
    """Get seasonal patterns for an API."""
    try:
        return await controller.get_seasonal_patterns(
            api_name,
            lookback_days
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))