from typing import Dict, List
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailProvider:
    def __init__(self, config: Dict):
        self.smtp_server = config['smtp_server']
        self.smtp_port = config['smtp_port']
        self.username = config['username']
        self.password = config['password']
        self.from_email = config['from_email']

    async def send_alert(self, alert_data: Dict, recipients: List[str]):
        message = MIMEMultipart()
        message['From'] = self.from_email
        message['To'] = ', '.join(recipients)
        message['Subject'] = f"SMART Alert: {alert_data['title']}"

        body = self._format_alert_body(alert_data)
        message.attach(MIMEText(body, 'html'))

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(message)

    def _format_alert_body(self, alert_data: Dict) -> str:
        return f"""
        <h2>{alert_data['title']}</h2>
        <p><strong>API:</strong> {alert_data['api_name']}</p>
        <p><strong>Severity:</strong> {alert_data['severity']}</p>
        <p><strong>Description:</strong> {alert_data['description']}</p>
        <p><strong>Time:</strong> {alert_data['timestamp']}</p>
        """