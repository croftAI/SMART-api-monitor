# core/processors/stream_processor.py

from typing import Dict, Optional, List
from datetime import datetime
import asyncio
from collections import deque
import logging
from core.storage.metric_buffer_mgmt import MetricBuffer
from core.calculators.health_analysis import HealthCalculator
from core.calculators.spike_detection import SpikeDetector


class StreamProcessor:
    """Real-time stream processing for API metrics."""

    def __init__(self, config: Dict):
        self.config = config
        self.metric_buffer = MetricBuffer()
        self.health_calculator = HealthCalculator()
        self.spike_detector = SpikeDetector()
        self.processing_queues: Dict[str, asyncio.Queue] = {}
        self.logger = logging.getLogger(__name__)

    async def process_metric(self, api_name: str, metric_data: Dict) -> Dict:
        """Process a single metric event."""
        try:
            # Ensure queue exists
            if api_name not in self.processing_queues:
                self.processing_queues[api_name] = asyncio.Queue()

            # Add to processing queue
            await self.processing_queues[api_name].put(metric_data)

            # Process metric
            processed_data = await self._process_single_metric(
                api_name,
                metric_data
            )

            # Store in buffer
            self.metric_buffer.add_metric(api_name, processed_data)

            return processed_data

        except Exception as e:
            self.logger.error(f"Error processing metric: {str(e)}")
            raise

    async def _process_single_metric(
            self,
            api_name: str,
            metric_data: Dict
    ) -> Dict:
        """Process individual metric data point."""
        # Calculate health score
        health_score = self.health_calculator.calculate_health_score(
            api_name,
            metric_data
        )

        # Detect spikes
        is_spike = self.spike_detector.detect_spike(
            api_name,
            metric_data
        )

        return {
            'api_name': api_name,
            'timestamp': metric_data['timestamp'],
            'original_metrics': metric_data['metrics'],
            'health_score': health_score,
            'is_spike': is_spike,
            'processed_at': datetime.now()
        }

    async def start_processing(self):
        """Start background processing tasks."""
        self.logger.info("Starting stream processor")
        processing_tasks = [
            self._process_queue(api_name, queue)
            for api_name, queue in self.processing_queues.items()
        ]
        await asyncio.gather(*processing_tasks)

    async def _process_queue(self, api_name: str, queue: asyncio.Queue):
        """Process metrics from queue."""
        while True:
            try:
                # Get batch of metrics
                metrics = []
                try:
                    while len(metrics) < self.config['batch_size']:
                        metric = await asyncio.wait_for(
                            queue.get(),
                            timeout=self.config['batch_timeout']
                        )
                        metrics.append(metric)
                except asyncio.TimeoutError:
                    pass

                if metrics:
                    # Process batch
                    await self._process_metric_batch(api_name, metrics)

            except Exception as e:
                self.logger.error(
                    f"Error processing queue for {api_name}: {str(e)}"
                )
                await asyncio.sleep(1)

    async def _process_metric_batch(
            self,
            api_name: str,
            metrics: List[Dict]
    ):
        """Process a batch of metrics together."""
        try:
            # Sort by timestamp
            metrics.sort(key=lambda x: x['timestamp'])

            # Process each metric
            processed_metrics = []
            for metric in metrics:
                processed = await self._process_single_metric(
                    api_name,
                    metric
                )
                processed_metrics.append(processed)

            # Store batch results
            self.metric_buffer.add_metric_batch(api_name, processed_metrics)

        except Exception as e:
            self.logger.error(f"Error processing batch: {str(e)}")
            raise