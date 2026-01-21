import boto3
from django.conf import settings

class SESEmailService:
    def __init__(self):
        self.client = boto3.client(
            'ses',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )

    def send_email(self, to_email, subject, body):
        response = self.client.send_email(
            Source=settings.AWS_SES_FROM_EMAIL,
            Destination={'ToAddresses': [to_email]},
            Message={
                'Subject': {'Data': subject},
                'Body': {'Html': {'Data': body}}
            }
        )
        return response
