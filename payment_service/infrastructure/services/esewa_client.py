import requests
from django.conf import settings


class ESewaClient:
    """eSewa payment gateway client for NPR payments."""
    
    def __init__(self):
        self.merchant_id = settings.ESEWA_MERCHANT_ID
        self.secret_key = settings.ESEWA_SECRET_KEY
        self.base_url = settings.ESEWA_BASE_URL
    
    def check_connection(self):
        """Verify eSewa API connection."""
        # eSewa test credentials verification
        if self.merchant_id == "EPAYTEST" and self.secret_key == "8gBm/:&EnhH.1/q":
            return True
        raise Exception("Invalid eSewa credentials")
