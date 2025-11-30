import uuid
from decimal import Decimal
from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from domain.subscription import Subscription, RecurringPayment
from application.subscription_service import SubscriptionService


class SubscriptionServiceTest(TestCase):
    """Test cases for SubscriptionService."""
    
    def setUp(self):
        self.service = SubscriptionService()
        self.user_id = uuid.uuid4()
    
    def test_create_subscription(self):
        """Test creating a new subscription."""
        subscription = self.service.create_subscription(
            user_id=self.user_id,
            plan_name="Premium Plan",
            amount=Decimal("99.99"),
            billing_cycle="monthly"
        )
        
        self.assertIsNotNone(subscription.id)
        self.assertEqual(subscription.user_id, self.user_id)
        self.assertEqual(subscription.plan_name, "Premium Plan")
        self.assertEqual(subscription.amount, Decimal("99.99"))
        self.assertEqual(subscription.billing_cycle, "monthly")
        self.assertEqual(subscription.status, "active")
    
    def test_pause_subscription(self):
        """Test pausing an active subscription."""
        subscription = Subscription.objects.create(
            user_id=self.user_id,
            plan_name="Test Plan",
            amount=Decimal("50.00"),
            billing_cycle="monthly",
            next_billing_date=timezone.now() + timedelta(days=30)
        )
        
        result = self.service.pause_subscription(subscription.id)
        
        self.assertEqual(result.status, "paused")
    
    def test_cancel_subscription(self):
        """Test cancelling a subscription."""
        subscription = Subscription.objects.create(
            user_id=self.user_id,
            plan_name="Test Plan",
            amount=Decimal("50.00"),
            billing_cycle="monthly",
            next_billing_date=timezone.now() + timedelta(days=30)
        )
        
        result = self.service.cancel_subscription(subscription.id)
        
        self.assertEqual(result.status, "cancelled")
    
    def test_get_user_subscriptions(self):
        """Test retrieving user subscriptions."""
        Subscription.objects.create(
            user_id=self.user_id,
            plan_name="Plan 1",
            amount=Decimal("50.00"),
            billing_cycle="monthly",
            next_billing_date=timezone.now() + timedelta(days=30)
        )
        Subscription.objects.create(
            user_id=self.user_id,
            plan_name="Plan 2",
            amount=Decimal("100.00"),
            billing_cycle="yearly",
            next_billing_date=timezone.now() + timedelta(days=365)
        )
        
        subscriptions = self.service.get_user_subscriptions(self.user_id)
        
        self.assertEqual(len(subscriptions), 2)


class RecurringPaymentServiceTest(TestCase):
    """Test cases for RecurringPaymentService."""
    
    def setUp(self):
        from application.subscription_service import RecurringPaymentService
        self.service = RecurringPaymentService()
        self.subscription = Subscription.objects.create(
            user_id=uuid.uuid4(),
            plan_name="Test Plan",
            amount=Decimal("50.00"),
            billing_cycle="monthly",
            next_billing_date=timezone.now() + timedelta(days=30)
        )
    
    def test_create_recurring_payment(self):
        """Test creating a recurring payment."""
        payment = self.service.create_recurring_payment(
            subscription_id=self.subscription.id,
            amount=Decimal("50.00"),
            billing_date=timezone.now(),
            payment_method="stripe"
        )
        
        self.assertIsNotNone(payment.id)
        self.assertEqual(payment.subscription_id, self.subscription.id)
        self.assertEqual(payment.amount, Decimal("50.00"))
        self.assertEqual(payment.status, "pending")
    
    def test_process_payment(self):
        """Test processing a recurring payment."""
        payment = RecurringPayment.objects.create(
            subscription_id=self.subscription.id,
            amount=Decimal("50.00"),
            billing_date=timezone.now(),
            payment_method="stripe"
        )
        
        result = self.service.process_payment(payment.id, "txn_123456")
        
        self.assertEqual(result.status, "completed")
        self.assertEqual(result.transaction_id, "txn_123456")
        self.assertIsNotNone(result.processed_at)
    
    def test_get_subscription_payments(self):
        """Test retrieving subscription payments."""
        RecurringPayment.objects.create(
            subscription_id=self.subscription.id,
            amount=Decimal("50.00"),
            billing_date=timezone.now(),
            payment_method="stripe"
        )
        RecurringPayment.objects.create(
            subscription_id=self.subscription.id,
            amount=Decimal("50.00"),
            billing_date=timezone.now() - timedelta(days=30),
            payment_method="stripe",
            status="completed"
        )
        
        payments = self.service.get_subscription_payments(self.subscription.id)
        
        self.assertEqual(len(payments), 2)


class BillingManagementServiceTest(TestCase):
    """Test cases for BillingManagementService."""
    
    def setUp(self):
        from application.subscription_service import BillingManagementService
        self.service = BillingManagementService()
        self.user_id = uuid.uuid4()
        self.subscription = Subscription.objects.create(
            user_id=self.user_id,
            plan_name="Test Plan",
            amount=Decimal("50.00"),
            billing_cycle="monthly",
            next_billing_date=timezone.now() + timedelta(days=1)
        )
    
    def test_get_due_subscriptions(self):
        """Test retrieving subscriptions due for billing."""
        due_subs = self.service.get_due_subscriptions()
        
        self.assertGreaterEqual(len(due_subs), 1)
        self.assertIn(self.subscription.id, [s.id for s in due_subs])
    
    def test_process_subscription_billing(self):
        """Test processing subscription billing."""
        payment = self.service.process_subscription_billing(
            self.subscription.id,
            payment_method="stripe"
        )
        
        self.assertIsNotNone(payment)
        self.assertEqual(payment.subscription_id, self.subscription.id)
        self.assertEqual(payment.amount, self.subscription.amount)
    
    def test_update_next_billing_date(self):
        """Test updating next billing date."""
        original_date = self.subscription.next_billing_date
        
        self.service.update_next_billing_date(self.subscription.id)
        
        updated_sub = Subscription.objects.get(id=self.subscription.id)
        self.assertGreater(updated_sub.next_billing_date, original_date)
