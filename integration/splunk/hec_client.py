import aiohttp
from typing import Dict, List, Optional
from datetime import datetime


class SplunkHECClient:
    def __init__(self, config: Dict):
        self.base_url = config['hec_url']
        self.token = config['token']
        self.index = config.get('index', 'main')
        self.source = config.get('source', 'api_monitor')
        self.batch_size = config.get('batch_size', 100)

    async def send_event(self, event: Dict) -> bool:
        """Send single event to Splunk HEC."""
        headers = {
            'Authorization': f'Splunk {self.token}',
            'Content-Type': 'application/json'
        }

        payload = {
            'time': int(datetime.now().timestamp()),
            'source': self.source,
            'sourcetype': '_json',
            'index': self.index,
            'event': event
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                    self.base_url,
                    json=payload,
                    headers=headers
            ) as response:
                return response.status == 200

    async def send_batch(self, events: List[Dict]) -> bool:
        """Send batch of events to Splunk HEC."""
        # Implementation for batch sending
        pass