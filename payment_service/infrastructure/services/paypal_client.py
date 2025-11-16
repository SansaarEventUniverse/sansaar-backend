import paypalrestsdk
from django.conf import settings


class PayPalClient:
    """PayPal payment gateway client for USD payments."""
    
    def __init__(self):
        self.api = paypalrestsdk.Api({
            "mode": settings.PAYPAL_MODE,
            "client_id": settings.PAYPAL_CLIENT_ID,
            "client_secret": settings.PAYPAL_CLIENT_SECRET
        })
    
    def check_connection(self):
        """Verify PayPal API connection."""
        try:
            access_token = self.api.get_access_token()
            if access_token:
                return True
            raise Exception("Failed to get access token")
        except Exception as e:
            raise Exception(f"PayPal connection failed: {str(e)}")
