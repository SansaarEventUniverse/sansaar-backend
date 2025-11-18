import stripe
from decimal import Decimal
from typing import Dict, Any
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
    
    def create_payment_intent(self, amount: Decimal, currency: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Create a payment intent."""
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),  # Convert to cents
                currency=currency.lower(),
                metadata=metadata
            )
            return {
                'success': True,
                'transaction_id': intent.id,
                'status': intent.status,
                'client_secret': intent.client_secret
            }
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def refund_payment(self, transaction_id: str, amount: Decimal) -> Dict[str, Any]:
        """Refund a payment."""
        try:
            refund = stripe.Refund.create(
                payment_intent=transaction_id,
                amount=int(amount * 100)
            )
            return {
                'success': True,
                'refund_id': refund.id,
                'status': refund.status
            }
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e)
            }
