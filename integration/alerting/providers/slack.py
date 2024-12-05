from typing import Dict
import aiohttp


class SlackProvider:
    def __init__(self, config: Dict):
        self.webhook_url = config['webhook_url']
        self.default_channel = config['default_channel']

    async def send_alert(self, alert_data: Dict, channel: str = None):
        message = self._format_message(alert_data)

        async with aiohttp.ClientSession() as session:
            await session.post(
                self.webhook_url,
                json={
                    'channel': channel or self.default_channel,
                    'blocks': message
                }
            )

    def _format_message(self, alert_data: Dict) -> List[Dict]:
        return [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"🚨 {alert_data['title']}"
                }
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*API:*\n{alert_data['api_name']}"},
                    {"type": "mrkdwn", "text": f"*Severity:*\n{alert_data['severity']}"}
                ]
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": alert_data['description']}
            }
        ]