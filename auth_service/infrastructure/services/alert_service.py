import json

import requests
from decouple import config
from django.core.mail import send_mail


class AlertService:
    def __init__(self):
        self.slack_webhook_url = config("SLACK_WEBHOOK_URL", default="")
        self.alert_email = config("ALERT_EMAIL", default="security@sansaar.com")

    def send_alert(self, alert_type: str, message: str, metadata: dict = None):
        email_sent = self._send_email_alert(alert_type, message, metadata)
        slack_sent = self._send_slack_alert(alert_type, message, metadata)
        return {"email_sent": email_sent, "slack_sent": slack_sent}

    def _send_email_alert(self, alert_type: str, message: str, metadata: dict = None):
        try:
            subject = f"Security Alert: {alert_type}"
            body = f"{message}\n\nMetadata: {json.dumps(metadata, indent=2)}" if metadata else message
            send_mail(subject, body, config("AWS_SES_FROM_EMAIL"), [self.alert_email])
            return True
        except Exception:
            return False

    def _send_slack_alert(self, alert_type: str, message: str, metadata: dict = None):
        if not self.slack_webhook_url:
            return False

        try:
            payload = {
                "text": f"🚨 *Security Alert: {alert_type}*",
                "blocks": [
                    {"type": "header", "text": {"type": "plain_text", "text": f"🚨 {alert_type}"}},
                    {"type": "section", "text": {"type": "mrkdwn", "text": message}},
                ],
            }

            if metadata:
                payload["blocks"].append(
                    {"type": "section", "text": {"type": "mrkdwn", "text": f"```{json.dumps(metadata, indent=2)}```"}}
                )

            response = requests.post(self.slack_webhook_url, json=payload, timeout=5)
            return response.status_code == 200
        except Exception:
            return False
