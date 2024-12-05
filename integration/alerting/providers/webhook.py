from typing import Dict
import aiohttp
import json
import hmac
import hashlib

class WebhookProvider:
    def __init__(self, config: Dict):
        self.endpoints = config['endpoints']
        self.secret = config.get('secret')

    async def send_alert(self, alert_data: Dict, endpoint_name: str):
        if endpoint_name not in self.endpoints:
            raise ValueError(f"Unknown endpoint: {endpoint_name}")

        payload = self._prepare_payload(alert_data)
        headers = self._generate_headers(payload)

        async with aiohttp.ClientSession() as session:
            await session.post(
                self.endpoints[endpoint_name],
                json=payload,
                headers=headers
            )

    def _prepare_payload(self, alert_data: Dict) -> Dict:
        return {
            "event_type": "alert",
            "data": alert_data,
            "timestamp": alert_data['timestamp']
        }

    def _generate_headers(self, payload: Dict) -> Dict:
        headers = {
            'Content-Type': 'application/json'
        }

        if self.secret:
            signature = hmac.new(
                self.secret.encode(),
                json.dumps(payload).encode(),
                hashlib.sha256
            ).hexdigest()
            headers['X-Signature'] = signature

        return headers