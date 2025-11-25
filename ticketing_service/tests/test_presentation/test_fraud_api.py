from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient
import uuid

from domain.fraud import FraudAlert, SecurityRule
from domain.order import Order


class FraudAPITest(TestCase):
    """Tests for fraud API endpoints."""
    
    def setUp(self):
        self.client = APIClient()
        
        rule = SecurityRule.objects.create(
            name='Test Rule',
            rule_type='velocity',
            threshold_value=5
        )
        
        FraudAlert.objects.create(
            order_id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            rule_id=rule.id,
            severity='high',
            description='Test alert',
            risk_score=80
        )
    
    def test_get_fraud_alerts(self):
        """Test getting fraud alerts."""
        response = self.client.get('/api/tickets/fraud/alerts/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('alerts', response.data)
        self.assertEqual(response.data['total_count'], 1)
    
    def test_get_security_report(self):
        """Test getting security report."""
        response = self.client.get('/api/tickets/security/report/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('total_alerts', response.data)
    
    def test_risk_assessment(self):
        """Test order risk assessment."""
        order = Order.objects.create(
            user_id=uuid.uuid4(),
            event_id=uuid.uuid4(),
            total_amount=Decimal('600.00'),
            status='pending'
        )
        
        response = self.client.post(f'/api/tickets/orders/{order.id}/risk-assessment/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('risk_score', response.data)
        self.assertIn('recommendation', response.data)
