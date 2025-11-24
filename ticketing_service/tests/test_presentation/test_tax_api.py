from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient
import uuid

from domain.tax import TaxRule, TaxCalculation
from domain.order import Order


class TaxAPITest(TestCase):
    """Tests for tax API endpoints."""
    
    def setUp(self):
        self.client = APIClient()
        self.event_id = uuid.uuid4()
        
        TaxRule.objects.create(
            name='US Sales Tax',
            country='US',
            tax_rate=Decimal('10.00')
        )
        
        self.order = Order.objects.create(
            user_id=uuid.uuid4(),
            event_id=self.event_id,
            total_amount=Decimal('100.00'),
            status='confirmed'
        )
    
    def test_calculate_tax(self):
        """Test calculating tax for order."""
        data = {'country': 'US'}
        
        response = self.client.post(
            f'/api/tickets/orders/{self.order.id}/calculate-tax/',
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['subtotal'], '100.00')
        self.assertEqual(response.data['tax_amount'], '10.00')
        self.assertEqual(response.data['total'], '110.00')
    
    def test_get_tax_report(self):
        """Test getting tax report."""
        # Create tax calculation first
        tax_rule = TaxRule.objects.first()
        TaxCalculation.objects.create(
            order_id=self.order.id,
            tax_rule_id=tax_rule.id,
            subtotal=Decimal('100.00'),
            tax_amount=Decimal('10.00')
        )
        
        response = self.client.get(f'/api/tickets/events/{self.event_id}/tax-report/')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['total_subtotal'], 100.0)
        self.assertEqual(response.data['total_tax_collected'], 10.0)
    
    def test_tax_compliance(self):
        """Test tax compliance check."""
        response = self.client.get(f'/api/tickets/events/{self.event_id}/tax-compliance/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('compliance_rate', response.data)
        self.assertIn('is_compliant', response.data)
