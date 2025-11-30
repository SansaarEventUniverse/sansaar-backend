import uuid
from decimal import Decimal
from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from domain.subscription import Subscription, RecurringPayment
from infrastructure.services.billing_engine import BillingEngine
from infrastructure.services.subscription_analytics import SubscriptionAnalytics
from infrastructure.services.billing_notification import BillingNotificationService


class BillingEngineTest(TestCase):
    """Test cases for BillingEngine."""
    
    def setUp(self):
        self.engine = BillingEngine()
        self.user_id = uuid.uuid4()
        self.subscription = Subscription.objects.create(
            user_id=self.user_id,
            plan_name="Test Plan",
            amount=Decimal("50.00"),
            billing_cycle="monthly",
            next_billing_date=timezone.now()
        )
    
    def test_process_due_subscriptions(self):
        """Test processing all due subscriptions."""
        results = self.engine.process_due_subscriptions()
        
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
    
    def test_charge_subscription(self):
        """Test charging a subscription."""
        payment = self.engine.charge_subscription(
            self.subscription.id,
            payment_method="stripe"
        )
        
        self.assertIsNotNone(payment)
        self.assertEqual(payment.subscription_id, self.subscription.id)
        self.assertEqual(payment.amount, self.subscription.amount)
    
    def test_handle_failed_payment(self):
        """Test handling failed payment."""
        payment = RecurringPayment.objects.create(
            subscription_id=self.subscription.id,
            amount=Decimal("50.00"),
            billing_date=timezone.now(),
            payment_method="stripe"
        )
        
        self.engine.handle_failed_payment(payment.id)
        
        updated_payment = RecurringPayment.objects.get(id=payment.id)
        self.assertEqual(updated_payment.status, "failed")


class SubscriptionAnalyticsTest(TestCase):
    """Test cases for SubscriptionAnalytics."""
    
    def setUp(self):
        self.analytics = SubscriptionAnalytics()
        self.user_id = uuid.uuid4()
        
        # Create test subscriptions
        Subscription.objects.create(
            user_id=self.user_id,
            plan_name="Plan 1",
            amount=Decimal("50.00"),
            billing_cycle="monthly",
            status="active",
            next_billing_date=timezone.now() + timedelta(days=30)
        )
        Subscription.objects.create(
            user_id=uuid.uuid4(),
            plan_name="Plan 2",
            amount=Decimal("100.00"),
            billing_cycle="yearly",
            status="cancelled",
            next_billing_date=timezone.now() + timedelta(days=365)
        )
    
    def test_get_active_subscriptions_count(self):
        """Test getting active subscriptions count."""
        count = self.analytics.get_active_subscriptions_count()
        
        self.assertGreaterEqual(count, 1)
    
    def test_get_monthly_recurring_revenue(self):
        """Test calculating monthly recurring revenue."""
        mrr = self.analytics.get_monthly_recurring_revenue()
        
        self.assertIsInstance(mrr, Decimal)
        self.assertGreater(mrr, Decimal("0"))
    
    def test_get_churn_rate(self):
        """Test calculating churn rate."""
        churn_rate = self.analytics.get_churn_rate()
        
        self.assertIsInstance(churn_rate, float)
        self.assertGreaterEqual(churn_rate, 0)
    
    def test_get_subscription_metrics(self):
        """Test getting comprehensive subscription metrics."""
        metrics = self.analytics.get_subscription_metrics()
        
        self.assertIn('active_count', metrics)
        self.assertIn('mrr', metrics)
        self.assertIn('churn_rate', metrics)


class BillingNotificationServiceTest(TestCase):
    """Test cases for BillingNotificationService."""
    
    def setUp(self):
        self.notification_service = BillingNotificationService()
        self.user_id = uuid.uuid4()
        self.subscription = Subscription.objects.create(
            user_id=self.user_id,
            plan_name="Test Plan",
            amount=Decimal("50.00"),
            billing_cycle="monthly",
            next_billing_date=timezone.now() + timedelta(days=3)
        )
    
    def test_send_upcoming_billing_notification(self):
        """Test sending upcoming billing notification."""
        result = self.notification_service.send_upcoming_billing_notification(
            self.subscription.id
        )
        
        self.assertTrue(result)
    
    def test_send_payment_success_notification(self):
        """Test sending payment success notification."""
        payment = RecurringPayment.objects.create(
            subscription_id=self.subscription.id,
            amount=Decimal("50.00"),
            billing_date=timezone.now(),
            payment_method="stripe",
            status="completed",
            transaction_id="txn_123"
        )
        
        result = self.notification_service.send_payment_success_notification(
            payment.id
        )
        
        self.assertTrue(result)
    
    def test_send_payment_failed_notification(self):
        """Test sending payment failed notification."""
        payment = RecurringPayment.objects.create(
            subscription_id=self.subscription.id,
            amount=Decimal("50.00"),
            billing_date=timezone.now(),
            payment_method="stripe",
            status="failed"
        )
        
        result = self.notification_service.send_payment_failed_notification(
            payment.id
        )
        
        self.assertTrue(result)
    
    def test_notify_subscriptions_due_soon(self):
        """Test notifying all subscriptions due soon."""
        results = self.notification_service.notify_subscriptions_due_soon()
        
        self.assertIsInstance(results, list)
