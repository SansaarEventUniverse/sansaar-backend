from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import logging

logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self):
        self.client = SendGridAPIClient(settings.SENDGRID_API_KEY)
        self.from_email = settings.SENDGRID_FROM_EMAIL
    
    def send_verification_email(self, to_email, verification_token, first_name):
        try:
            verification_url = f"http://{settings.ALLOWED_HOSTS[0]}/verify-email?token={verification_token}"
            
            message = Mail(
                from_email=self.from_email,
                to_emails=to_email
            )
            message.template_id = settings.SENDGRID_VERIFICATION_TEMPLATE_ID
            message.dynamic_template_data = {
                'first_name': first_name,
                'verification_url': verification_url
            }
            
            response = self.client.send(message)
            return response.status_code == 202
        except Exception as e:
            logger.error(f"Failed to send verification email: {str(e)}")
            return False
