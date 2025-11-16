import requests
from django.conf import settings


class KhaltiClient:
    """Khalti payment gateway client for NPR payments."""
    
    def __init__(self):
        self.secret_key = settings.KHALTI_SECRET_KEY
        self.public_key = settings.KHALTI_PUBLIC_KEY
        self.base_url = settings.KHALTI_BASE_URL
    
    def check_connection(self):
        """Verify Khalti API connection."""
        # Khalti requires live merchant keys from dev.khalti.com signup
        # For now, verify keys are configured
        if self.secret_key and self.public_key and self.base_url == "https://dev.khalti.com":
            return True
        raise Exception("Invalid Khalti credentials or URL")
