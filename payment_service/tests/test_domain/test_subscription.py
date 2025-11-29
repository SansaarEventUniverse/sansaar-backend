from decimal import Decimal
from datetime import timedelta
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
import uuid

from domain.subscription import Subscription, RecurringPayment


class SubscriptionModelTest(TestCase):
    """Tests for Subscription model."""
    
    def setUp(self):
        self.user_id = uuid.uuid4()
        self.next_billing = timezone.now() + timedelta(days=30)
    
    def test_create_subscription(self):
        """Test creating a subscription."""
        sub = Subscription.objects.create(
            user_id=self.user_id,
            plan_name='Premium Plan',
            amount=Decimal('29.99'),
            billing_cycle='monthly',
            next_billing_date=self.next_billing
        )
        
        self.assertEqual(sub.status, 'active')
        self.assertTrue(sub.is_active())
    
    def test_pause_subscription(self):
        """Test pausing subscription."""
        sub = Subscription.objects.create(
            user_id=self.user_id,
            plan_name='Basic Plan',
            amount=Decimal('9.99'),
            billing_cycle='monthly',
            next_billing_date=self.next_billing
        )
        
        sub.pause()
        self.assertEqual(sub.status, 'paused')
        self.assertFalse(sub.is_active())
    
    def test_cancel_subscription(self):
        """Test cancelling subscription."""
        sub = Subscription.objects.create(
            user_id=self.user_id,
            plan_name='Pro Plan',
            amount=Decimal('49.99'),
            billing_cycle='yearly',
            next_billing_date=self.next_billing
        )
        
        sub.cancel()
        self.assertEqual(sub.status, 'cancelled')
    
    def test_calculate_next_billing_monthly(self):
        """Test calculating next billing date for monthly."""
        sub = Subscription.objects.create(
            user_id=self.user_id,
            plan_name='Monthly Plan',
            amount=Decimal('19.99'),
            billing_cycle='monthly',
            next_billing_date=self.next_billing
        )
        
        original_date = sub.next_billing_date
        sub.calculate_next_billing_date()
        
        self.assertEqual(
            (sub.next_billing_date - original_date).days,
            30
        )


class RecurringPaymentModelTest(TestCase):
    """Tests for RecurringPayment model."""
    
    def setUp(self):
        self.subscription_id = uuid.uuid4()
        self.billing_date = timezone.now()
    
    def test_create_recurring_payment(self):
        """Test creating recurring payment."""
        payment = RecurringPayment.objects.create(
            subscription_id=self.subscription_id,
            amount=Decimal('29.99'),
            billing_date=self.billing_date,
            payment_method='credit_card'
        )
        
        self.assertEqual(payment.status, 'pending')
    
    def test_process_payment(self):
        """Test processing payment."""
        payment = RecurringPayment.objects.create(
            subscription_id=self.subscription_id,
            amount=Decimal('19.99'),
            billing_date=self.billing_date,
            payment_method='credit_card'
        )
        
        payment.process('txn_123')
        
        self.assertEqual(payment.status, 'completed')
        self.assertEqual(payment.transaction_id, 'txn_123')
        self.assertIsNotNone(payment.processed_at)
    
    def test_fail_payment(self):
        """Test failing payment."""
        payment = RecurringPayment.objects.create(
            subscription_id=self.subscription_id,
            amount=Decimal('39.99'),
            billing_date=self.billing_date,
            payment_method='credit_card'
        )
        
        payment.fail()
        self.assertEqual(payment.status, 'failed')
    
    def test_cannot_process_twice(self):
        """Test cannot process payment twice."""
        payment = RecurringPayment.objects.create(
            subscription_id=self.subscription_id,
            amount=Decimal('49.99'),
            billing_date=self.billing_date,
            payment_method='credit_card'
        )
        
        payment.process('txn_456')
        
        with self.assertRaises(ValidationError):
            payment.process('txn_789')
