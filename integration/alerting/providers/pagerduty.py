from typing import Dict
import aiohttp


class PagerDutyProvider:
    def __init__(self, config: Dict):
        self.api_key = config['api_key']
        self.service_id = config['service_id']

    async def send_alert(self, alert_data: Dict):
        """Send alert to PagerDuty."""
        headers = {
            'Authorization': f'Token token={self.api_key}',
            'Content-Type': 'application/json'
        }

        payload = {
            'incident': {
                'type': 'incident',
                'title': alert_data['title'],
                'service': {
                    'id': self.service_id,
                    'type': 'service_reference'
                },
                'urgency': alert_data.get('urgency', 'high'),
                'body': {
                    'type': 'incident_body',
                    'details': alert_data['description']
                }
            }
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                    'https://api.pagerduty.com/incidents',
                    json=payload,
                    headers=headers
            ) as response:
                return response.status == 201