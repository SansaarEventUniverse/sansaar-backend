import uuid
from typing import List
from datetime import timedelta
from django.utils import timezone
from domain.subscription import Subscription, RecurringPayment


class BillingNotificationService:
    """Service for sending billing notifications."""
    
    def send_upcoming_billing_notification(
        self,
        subscription_id: uuid.UUID
    ) -> bool:
        """Send notification for upcoming billing."""
        try:
            subscription = Subscription.objects.get(id=subscription_id)
            
            # In production, integrate with email/notification service
            # For now, just log the notification
            print(f"Upcoming billing notification sent for subscription {subscription_id}")
            print(f"User: {subscription.user_id}, Amount: {subscription.amount}")
            print(f"Next billing date: {subscription.next_billing_date}")
            
            return True
        except Exception as e:
            print(f"Failed to send notification: {str(e)}")
            return False
    
    def send_payment_success_notification(
        self,
        payment_id: uuid.UUID
    ) -> bool:
        """Send notification for successful payment."""
        try:
            payment = RecurringPayment.objects.get(id=payment_id)
            subscription = Subscription.objects.get(id=payment.subscription_id)
            
            print(f"Payment success notification sent for payment {payment_id}")
            print(f"User: {subscription.user_id}, Amount: {payment.amount}")
            print(f"Transaction ID: {payment.transaction_id}")
            
            return True
        except Exception as e:
            print(f"Failed to send notification: {str(e)}")
            return False
    
    def send_payment_failed_notification(
        self,
        payment_id: uuid.UUID
    ) -> bool:
        """Send notification for failed payment."""
        try:
            payment = RecurringPayment.objects.get(id=payment_id)
            subscription = Subscription.objects.get(id=payment.subscription_id)
            
            print(f"Payment failed notification sent for payment {payment_id}")
            print(f"User: {subscription.user_id}, Amount: {payment.amount}")
            
            return True
        except Exception as e:
            print(f"Failed to send notification: {str(e)}")
            return False
    
    def notify_subscriptions_due_soon(self, days: int = 3) -> List[uuid.UUID]:
        """Notify users about subscriptions due soon."""
        threshold_date = timezone.now() + timedelta(days=days)
        
        due_soon = Subscription.objects.filter(
            status='active',
            next_billing_date__lte=threshold_date,
            next_billing_date__gte=timezone.now()
        )
        
        notified = []
        for subscription in due_soon:
            if self.send_upcoming_billing_notification(subscription.id):
                notified.append(subscription.id)
        
        return notified
