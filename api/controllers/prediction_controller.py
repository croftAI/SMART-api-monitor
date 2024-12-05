# api/controllers/prediction_controller.py

from typing import Dict, Optional, List
from datetime import datetime, timedelta
from fastapi import HTTPException
from analysis.predictive.forecasting import TrafficForecaster
from analysis.predictive.threshold_predictor import ThresholdPredictor


class PredictionController:
    """Controller for prediction-related operations."""

    def __init__(self):
        self.traffic_forecaster = TrafficForecaster()
        self.threshold_predictor = ThresholdPredictor()

    async def predict_traffic(
            self,
            api_name: str,
            horizon_hours: int = 24
    ) -> Dict:
        """Predict traffic patterns for an API."""
        try:
            forecast = await self.traffic_forecaster.forecast_traffic(
                api_name,
                horizon_hours
            )

            return {
                'api_name': api_name,
                'timestamp': datetime.now().isoformat(),
                'horizon_hours': horizon_hours,
                'predictions': forecast
            }
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Traffic prediction failed: {str(e)}"
            )

    async def predict_thresholds(
            self,
            api_name: str,
            forecast: Dict
    ) -> Dict:
        """Predict optimal thresholds based on forecasted conditions."""
        try:
            predictions = await self.threshold_predictor.predict_thresholds(
                api_name,
                forecast
            )

            return {
                'api_name': api_name,
                'timestamp': datetime.now().isoformat(),
                'threshold_predictions': predictions
            }
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Threshold prediction failed: {str(e)}"
            )

    async def get_seasonal_patterns(
            self,
            api_name: str,
            lookback_days: int = 30
    ) -> Dict:
        """Get seasonal patterns for an API."""
        try:
            patterns = await self.traffic_forecaster.analyze_seasonality(
                api_name,
                lookback_days
            )

            return {
                'api_name': api_name,
                'timestamp': datetime.now().isoformat(),
                'seasonal_patterns': patterns
            }
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Seasonal analysis failed: {str(e)}"
            )