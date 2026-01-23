import firebase_admin
from firebase_admin import credentials, messaging
from django.conf import settings

class FCMService:
    def __init__(self):
        if not firebase_admin._apps:
            cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred)

    def send_push_notification(self, token, title, body, data=None):
        message = messaging.Message(
            notification=messaging.Notification(title=title, body=body),
            data=data or {},
            token=token
        )
        response = messaging.send(message)
        return response
