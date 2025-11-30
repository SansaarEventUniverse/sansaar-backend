import uuid
from decimal import Decimal
from datetime import timedelta
from typing import List
from django.utils import timezone
from django.core.exceptions import ValidationError
from domain.subscription import Subscription, RecurringPayment


class SubscriptionService:
    """Service for managing subscriptions."""
    
    def create_subscription(
        self,
        user_id: uuid.UUID,
        plan_name: str,
        amount: Decimal,
        billing_cycle: str
    ) -> Subscription:
        """Create a new subscription."""
        next_billing_date = self._calculate_next_billing_date(billing_cycle)
        
        subscription = Subscription.objects.create(
            user_id=user_id,
            plan_name=plan_name,
            amount=amount,
            billing_cycle=billing_cycle,
            next_billing_date=next_billing_date
        )
        return subscription
    
    def pause_subscription(self, subscription_id: uuid.UUID) -> Subscription:
        """Pause an active subscription."""
        subscription = Subscription.objects.get(id=subscription_id)
        subscription.pause()
        return subscription
    
    def cancel_subscription(self, subscription_id: uuid.UUID) -> Subscription:
        """Cancel a subscription."""
        subscription = Subscription.objects.get(id=subscription_id)
        subscription.cancel()
        return subscription
    
    def get_user_subscriptions(self, user_id: uuid.UUID) -> List[Subscription]:
        """Get all subscriptions for a user."""
        return list(Subscription.objects.filter(user_id=user_id))
    
    def _calculate_next_billing_date(self, billing_cycle: str):
        """Calculate next billing date based on cycle."""
        now = timezone.now()
        if billing_cycle == 'monthly':
            return now + timedelta(days=30)
        elif billing_cycle == 'quarterly':
            return now + timedelta(days=90)
        elif billing_cycle == 'yearly':
            return now + timedelta(days=365)
        raise ValidationError(f"Invalid billing cycle: {billing_cycle}")


class RecurringPaymentService:
    """Service for managing recurring payments."""
    
    def create_recurring_payment(
        self,
        subscription_id: uuid.UUID,
        amount: Decimal,
        billing_date,
        payment_method: str
    ) -> RecurringPayment:
        """Create a new recurring payment."""
        payment = RecurringPayment.objects.create(
            subscription_id=subscription_id,
            amount=amount,
            billing_date=billing_date,
            payment_method=payment_method
        )
        return payment
    
    def process_payment(
        self,
        payment_id: uuid.UUID,
        transaction_id: str
    ) -> RecurringPayment:
        """Process a recurring payment."""
        payment = RecurringPayment.objects.get(id=payment_id)
        payment.process(transaction_id)
        return payment
    
    def get_subscription_payments(
        self,
        subscription_id: uuid.UUID
    ) -> List[RecurringPayment]:
        """Get all payments for a subscription."""
        return list(RecurringPayment.objects.filter(subscription_id=subscription_id))


class BillingManagementService:
    """Service for managing billing operations."""
    
    def __init__(self):
        self.recurring_payment_service = RecurringPaymentService()
    
    def get_due_subscriptions(self) -> List[Subscription]:
        """Get subscriptions due for billing."""
        now = timezone.now()
        return list(Subscription.objects.filter(
            status='active',
            next_billing_date__lte=now + timedelta(days=1)
        ))
    
    def process_subscription_billing(
        self,
        subscription_id: uuid.UUID,
        payment_method: str
    ) -> RecurringPayment:
        """Process billing for a subscription."""
        subscription = Subscription.objects.get(id=subscription_id)
        
        payment = self.recurring_payment_service.create_recurring_payment(
            subscription_id=subscription.id,
            amount=subscription.amount,
            billing_date=timezone.now(),
            payment_method=payment_method
        )
        return payment
    
    def update_next_billing_date(self, subscription_id: uuid.UUID) -> Subscription:
        """Update next billing date for a subscription."""
        subscription = Subscription.objects.get(id=subscription_id)
        subscription.calculate_next_billing_date()
        return subscription
