import uuid
from typing import List, Dict
from decimal import Decimal
from django.utils import timezone
from django.db.models import Q
from domain.subscription import Subscription, RecurringPayment
from application.subscription_service import (
    BillingManagementService,
    RecurringPaymentService
)


class BillingEngine:
    """Engine for processing subscription billing."""
    
    def __init__(self):
        self.billing_service = BillingManagementService()
        self.payment_service = RecurringPaymentService()
    
    def process_due_subscriptions(self) -> List[Dict]:
        """Process all subscriptions due for billing."""
        due_subscriptions = self.billing_service.get_due_subscriptions()
        results = []
        
        for subscription in due_subscriptions:
            try:
                payment = self.charge_subscription(
                    subscription.id,
                    payment_method="stripe"  # Default payment method
                )
                results.append({
                    'subscription_id': subscription.id,
                    'payment_id': payment.id,
                    'status': 'success'
                })
            except Exception as e:
                results.append({
                    'subscription_id': subscription.id,
                    'status': 'failed',
                    'error': str(e)
                })
        
        return results
    
    def charge_subscription(
        self,
        subscription_id: uuid.UUID,
        payment_method: str
    ) -> RecurringPayment:
        """Charge a subscription."""
        payment = self.billing_service.process_subscription_billing(
            subscription_id,
            payment_method
        )
        
        # Simulate payment processing
        transaction_id = f"txn_{uuid.uuid4().hex[:12]}"
        self.payment_service.process_payment(payment.id, transaction_id)
        
        # Update next billing date
        self.billing_service.update_next_billing_date(subscription_id)
        
        return payment
    
    def handle_failed_payment(self, payment_id: uuid.UUID) -> None:
        """Handle a failed payment."""
        payment = RecurringPayment.objects.get(id=payment_id)
        payment.fail()
