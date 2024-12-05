# analysis/ml_models/canary_manager.py

from typing import Dict, Optional, Callable, List
from datetime import datetime, timedelta
import asyncio
import numpy as np
from logging import Logger
import json


class DeploymentMetrics:
    def __init__(self):
        self.error_rate: float = 0.0
        self.latency: float = 0.0
        self.success_rate: float = 0.0
        self.timestamp: datetime = datetime.now()


class CanaryDeployment:
    def __init__(self, config: Dict, logger: Logger):
        self.config = config
        self.logger = logger
        self.current_percentage = 0
        self.start_time = None
        self.metrics_history: List[Dict] = []
        self.status = 'pending'
        self.deployment_id = None
        self._rollback_in_progress = False

    async def start_deployment(
            self,
            new_model: any,
            current_model: any,
            metric_collector: Callable
    ) -> bool:
        """Start canary deployment process."""
        self.deployment_id = f"deploy_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.start_time = datetime.now()
        self.current_percentage = self.config['initial_percentage']
        self.status = 'in_progress'
        self.logger.info(f"Starting canary deployment {self.deployment_id}")

        try:
            while self.current_percentage < 100:
                self.logger.info(
                    f"Canary at {self.current_percentage}% for {self.deployment_id}"
                )

                # Collect metrics for current distribution
                metrics = await self._collect_deployment_metrics(
                    new_model,
                    current_model,
                    metric_collector
                )

                # Store metrics
                self._store_metrics(metrics)

                # Evaluate deployment health
                health_check = self._is_deployment_healthy(metrics)
                if health_check['healthy']:
                    # Increment canary percentage
                    await self._increment_deployment()
                else:
                    # Rollback if unhealthy
                    self.logger.warning(
                        f"Deployment {self.deployment_id} unhealthy: {health_check['reason']}"
                    )
                    await self._rollback_deployment(health_check['reason'])
                    return False

                # Check if deployment is taking too long
                if self._deployment_timeout_reached():
                    await self._rollback_deployment("Deployment timeout reached")
                    return False

                # Wait for next increment interval
                await asyncio.sleep(
                    self.config['increment_interval_minutes'] * 60
                )

            # Deployment completed successfully
            await self._complete_deployment()
            return True

        except Exception as e:
            self.logger.error(f"Deployment error: {str(e)}")
            await self._rollback_deployment(f"Error: {str(e)}")
            raise e

    async def _collect_deployment_metrics(
            self,
            new_model: any,
            current_model: any,
            metric_collector: Callable
    ) -> Dict:
        """Collect metrics for current deployment state."""
        canary_metrics = []
        control_metrics = []

        collection_duration = timedelta(
            minutes=self.config['increment_interval_minutes']
        )
        start_time = datetime.now()

        while datetime.now() - start_time < collection_duration:
            # Get current metrics
            current_metrics = await metric_collector()

            # Route request based on canary percentage
            if np.random.random() < (self.current_percentage / 100):
                prediction = await self._safe_predict(
                    new_model,
                    current_metrics,
                    'canary'
                )
                canary_metrics.append(prediction)
            else:
                prediction = await self._safe_predict(
                    current_model,
                    current_metrics,
                    'control'
                )
                control_metrics.append(prediction)

            await asyncio.sleep(1)

        return {
            'canary': self._aggregate_metrics(canary_metrics),
            'control': self._aggregate_metrics(control_metrics),
            'timestamp': datetime.now()
        }

    async def _safe_predict(
            self,
            model: any,
            metrics: Dict,
            group: str
    ) -> Dict:
        """Safely make prediction with error handling."""
        try:
            start_time = datetime.now()
            prediction = await model.predict(metrics)
            latency = (datetime.now() - start_time).total_seconds()

            return {
                'success': True,
                'latency': latency,
                'prediction': prediction,
                'error': None
            }
        except Exception as e:
            self.logger.error(f"Prediction error in {group}: {str(e)}")
            return {
                'success': False,
                'latency': 0,
                'prediction': None,
                'error': str(e)
            }

    def _aggregate_metrics(self, metrics: List[Dict]) -> Dict:
        """Aggregate collected metrics."""
        if not metrics:
            return {}

        successful_predictions = [m for m in metrics if m['success']]
        total_predictions = len(metrics)

        return {
            'error_rate': 1 - (len(successful_predictions) / total_predictions),
            'average_latency': np.mean([m['latency'] for m in successful_predictions]) if successful_predictions else 0,
            'success_rate': len(successful_predictions) / total_predictions,
            'total_requests': total_predictions
        }

    def _is_deployment_healthy(self, metrics: Dict) -> Dict:
        """Evaluate if current deployment state is healthy."""
        threshold = self.config['rollback_threshold']

        # Check each monitored metric
        for metric_name in self.config['monitoring_metrics']:
            canary_value = metrics['canary'].get(metric_name)
            control_value = metrics['control'].get(metric_name)

            if canary_value is None or control_value is None:
                return {
                    'healthy': False,
                    'reason': f"Missing metric: {metric_name}"
                }

            # Calculate relative difference
            diff = abs(canary_value - control_value) / control_value
            if diff > (1 - threshold):
                return {
                    'healthy': False,
                    'reason': f"Metric {metric_name} exceeded threshold: {diff:.2f} > {1 - threshold:.2f}"
                }

        return {'healthy': True, 'reason': None}

    async def _increment_deployment(self):
        """Increment the canary percentage."""
        self.current_percentage = min(
            100,
            self.current_percentage + self.config['increment_percentage']
        )

        self.logger.info(
            f"Incremented deployment {self.deployment_id} to {self.current_percentage}%"
        )

    async def _rollback_deployment(self, reason: str):
        """Roll back canary deployment."""
        if self._rollback_in_progress:
            return

        self._rollback_in_progress = True
        self.status = 'rolling_back'

        self.logger.warning(
            f"Rolling back deployment {self.deployment_id}. Reason: {reason}"
        )

        # Store rollback event
        self.metrics_history.append({
            'timestamp': datetime.now(),
            'event': 'rollback',
            'reason': reason,
            'percentage': self.current_percentage
        })

        # Reset to 0%
        self.current_percentage = 0
        self.status = 'rolled_back'

        # Save deployment history
        await self._save_deployment_history()

    async def _complete_deployment(self):
        """Complete the deployment successfully."""
        self.status = 'completed'
        self.logger.info(f"Deployment {self.deployment_id} completed successfully")

        # Store completion event
        self.metrics_history.append({
            'timestamp': datetime.now(),
            'event': 'completion',
            'percentage': 100
        })

        # Save deployment history
        await self._save_deployment_history()

    def _deployment_timeout_reached(self) -> bool:
        """Check if deployment has exceeded maximum allowed time."""
        if not self.start_time:
            return False

        max_duration = timedelta(
            hours=self.config.get('max_deployment_hours', 24)
        )
        return datetime.now() - self.start_time > max_duration

    def _store_metrics(self, metrics: Dict):
        """Store metrics in deployment history."""
        self.metrics_history.append({
            'timestamp': metrics['timestamp'],
            'percentage': self.current_percentage,
            'canary': metrics['canary'],
            'control': metrics['control']
        })

    async def _save_deployment_history(self):
        """Save deployment history to file."""
        history_file = f"deployments/{self.deployment_id}_history.json"

        history = {
            'deployment_id': self.deployment_id,
            'start_time': self.start_time.isoformat(),
            'end_time': datetime.now().isoformat(),
            'status': self.status,
            'metrics_history': [
                {**m, 'timestamp': m['timestamp'].isoformat()}
                for m in self.metrics_history
            ]
        }

        try:
            with open(history_file, 'w') as f:
                json.dump(history, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save deployment history: {str(e)}")

    def get_deployment_status(self) -> Dict:
        """Get current deployment status."""
        return {
            'deployment_id': self.deployment_id,
            'status': self.status,
            'current_percentage': self.current_percentage,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'duration': str(datetime.now() - self.start_time) if self.start_time else None,
            'metrics_count': len(self.metrics_history)
        }