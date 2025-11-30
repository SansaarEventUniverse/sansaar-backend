import uuid
from decimal import Decimal
from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from domain.subscription import Subscription, RecurringPayment


class SubscriptionAPITest(TestCase):
    """Test cases for Subscription API endpoints."""
    
    def setUp(self):
        self.client = APIClient()
        self.user_id = uuid.uuid4()
    
    def test_create_subscription(self):
        """Test creating a subscription via API."""
        data = {
            'user_id': str(self.user_id),
            'plan_name': 'Premium Plan',
            'amount': '99.99',
            'billing_cycle': 'monthly'
        }
        
        response = self.client.post('/api/payments/subscriptions/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertEqual(response.data['plan_name'], 'Premium Plan')
        self.assertEqual(response.data['status'], 'active')
    
    def test_list_user_subscriptions(self):
        """Test listing user subscriptions."""
        Subscription.objects.create(
            user_id=self.user_id,
            plan_name='Plan 1',
            amount=Decimal('50.00'),
            billing_cycle='monthly',
            next_billing_date=timezone.now() + timedelta(days=30)
        )
        
        response = self.client.get(f'/api/payments/subscriptions/?user_id={self.user_id}')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_pause_subscription(self):
        """Test pausing a subscription."""
        subscription = Subscription.objects.create(
            user_id=self.user_id,
            plan_name='Test Plan',
            amount=Decimal('50.00'),
            billing_cycle='monthly',
            next_billing_date=timezone.now() + timedelta(days=30)
        )
        
        response = self.client.put(
            f'/api/payments/subscriptions/{subscription.id}/',
            {'action': 'pause'},
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'paused')
    
    def test_cancel_subscription(self):
        """Test cancelling a subscription."""
        subscription = Subscription.objects.create(
            user_id=self.user_id,
            plan_name='Test Plan',
            amount=Decimal('50.00'),
            billing_cycle='monthly',
            next_billing_date=timezone.now() + timedelta(days=30)
        )
        
        response = self.client.put(
            f'/api/payments/subscriptions/{subscription.id}/',
            {'action': 'cancel'},
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'cancelled')
    
    def test_get_billing_history(self):
        """Test retrieving billing history."""
        subscription = Subscription.objects.create(
            user_id=self.user_id,
            plan_name='Test Plan',
            amount=Decimal('50.00'),
            billing_cycle='monthly',
            next_billing_date=timezone.now() + timedelta(days=30)
        )
        
        RecurringPayment.objects.create(
            subscription_id=subscription.id,
            amount=Decimal('50.00'),
            billing_date=timezone.now(),
            payment_method='stripe',
            status='completed',
            transaction_id='txn_123'
        )
        
        response = self.client.get(
            f'/api/payments/subscriptions/{subscription.id}/billing/'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['status'], 'completed')
