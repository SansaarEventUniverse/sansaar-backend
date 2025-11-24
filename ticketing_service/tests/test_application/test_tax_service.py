from decimal import Decimal
from django.test import TestCase
import uuid

from domain.tax import TaxRule, TaxCalculation
from domain.order import Order
from application.tax_service import (
    TaxCalculationService,
    TaxComplianceService,
    TaxReportingService
)


class TaxCalculationServiceTest(TestCase):
    """Tests for TaxCalculationService."""
    
    def setUp(self):
        self.service = TaxCalculationService()
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
    
    def test_calculate_for_order(self):
        """Test calculating tax for order."""
        calc = self.service.calculate_for_order(self.order, 'US')
        
        self.assertEqual(calc.subtotal, Decimal('100.00'))
        self.assertEqual(calc.tax_amount, Decimal('10.00'))
        self.assertEqual(calc.total, Decimal('110.00'))


class TaxComplianceServiceTest(TestCase):
    """Tests for TaxComplianceService."""
    
    def setUp(self):
        self.service = TaxComplianceService()
        self.event_id = uuid.uuid4()
        
        tax_rule = TaxRule.objects.create(
            name='Tax',
            tax_rate=Decimal('10.00')
        )
        
        # Create orders
        for i in range(10):
            order = Order.objects.create(
                user_id=uuid.uuid4(),
                event_id=self.event_id,
                total_amount=Decimal('100.00'),
                status='confirmed'
            )
            
            # Tax only 9 out of 10 orders
            if i < 9:
                TaxCalculation.objects.create(
                    order_id=order.id,
                    tax_rule_id=tax_rule.id,
                    subtotal=Decimal('100.00'),
                    tax_amount=Decimal('10.00')
                )
    
    def test_check_compliance(self):
        """Test checking tax compliance."""
        compliance = self.service.check_compliance(self.event_id)
        
        self.assertEqual(compliance['total_orders'], 10)
        self.assertEqual(compliance['taxed_orders'], 9)
        self.assertEqual(compliance['untaxed_orders'], 1)
        self.assertEqual(compliance['compliance_rate'], 90.0)
        self.assertFalse(compliance['is_compliant'])


class TaxReportingServiceTest(TestCase):
    """Tests for TaxReportingService."""
    
    def setUp(self):
        self.service = TaxReportingService()
        self.event_id = uuid.uuid4()
        
        tax_rule = TaxRule.objects.create(
            name='Tax',
            tax_rate=Decimal('10.00')
        )
        
        order = Order.objects.create(
            user_id=uuid.uuid4(),
            event_id=self.event_id,
            total_amount=Decimal('100.00'),
            status='confirmed'
        )
        
        TaxCalculation.objects.create(
            order_id=order.id,
            tax_rule_id=tax_rule.id,
            subtotal=Decimal('100.00'),
            tax_amount=Decimal('10.00')
        )
    
    def test_generate_report(self):
        """Test generating tax report."""
        report = self.service.generate_report(self.event_id)
        
        self.assertEqual(report['total_subtotal'], Decimal('100.00'))
        self.assertEqual(report['total_tax_collected'], Decimal('10.00'))
        self.assertEqual(report['total_with_tax'], Decimal('110.00'))
        self.assertEqual(report['total_transactions'], 1)
