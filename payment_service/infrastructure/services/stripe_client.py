import stripe
from django.conf import settings


class StripeClient:
    """Stripe payment gateway client for USD payments."""
    
    def __init__(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        self.publishable_key = settings.STRIPE_PUBLISHABLE_KEY
    
    def check_connection(self):
        """Verify Stripe API connection."""
        try:
            stripe.Account.retrieve()
            return True
        except Exception as e:
            raise Exception(f"Stripe connection failed: {str(e)}")
