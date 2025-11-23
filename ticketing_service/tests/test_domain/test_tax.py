from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
import uuid

from domain.tax import TaxRule, TaxCalculation


class TaxRuleModelTest(TestCase):
    """Tests for TaxRule model."""
    
    def test_create_tax_rule(self):
        """Test creating a tax rule."""
        rule = TaxRule.objects.create(
            name='Sales Tax',
            country='US',
            state='CA',
            tax_rate=Decimal('8.50')
        )
        
        self.assertEqual(rule.tax_rate, Decimal('8.50'))
        self.assertTrue(rule.is_active)
    
    def test_calculate_percentage_tax(self):
        """Test calculating percentage tax."""
        rule = TaxRule.objects.create(
            name='VAT',
            tax_rate=Decimal('20.00')
        )
        
        tax = rule.calculate_tax(Decimal('100.00'))
        self.assertEqual(tax, Decimal('20.00'))
    
    def test_calculate_fixed_tax(self):
        """Test calculating fixed tax."""
        rule = TaxRule.objects.create(
            name='Fixed Tax',
            tax_type='fixed',
            tax_rate=Decimal('5.00')
        )
        
        tax = rule.calculate_tax(Decimal('100.00'))
        self.assertEqual(tax, Decimal('5.00'))
    
    def test_negative_rate_validation(self):
        """Test negative rate validation."""
        rule = TaxRule(
            name='Invalid',
            tax_rate=Decimal('-10.00')
        )
        
        with self.assertRaises(ValidationError):
            rule.clean()
    
    def test_excessive_percentage_validation(self):
        """Test excessive percentage validation."""
        rule = TaxRule(
            name='Invalid',
            tax_rate=Decimal('150.00')
        )
        
        with self.assertRaises(ValidationError):
            rule.clean()


class TaxCalculationModelTest(TestCase):
    """Tests for TaxCalculation model."""
    
    def setUp(self):
        self.order_id = uuid.uuid4()
        self.tax_rule = TaxRule.objects.create(
            name='Sales Tax',
            tax_rate=Decimal('10.00')
        )
    
    def test_create_tax_calculation(self):
        """Test creating tax calculation."""
        calc = TaxCalculation.objects.create(
            order_id=self.order_id,
            tax_rule_id=self.tax_rule.id,
            subtotal=Decimal('100.00'),
            tax_amount=Decimal('10.00')
        )
        
        self.assertEqual(calc.total, Decimal('110.00'))
    
    def test_calculate_total(self):
        """Test total calculation."""
        calc = TaxCalculation(
            order_id=self.order_id,
            tax_rule_id=self.tax_rule.id,
            subtotal=Decimal('200.00'),
            tax_amount=Decimal('20.00')
        )
        
        total = calc.calculate_total()
        self.assertEqual(total, Decimal('220.00'))
    
    def test_negative_subtotal_validation(self):
        """Test negative subtotal validation."""
        calc = TaxCalculation(
            order_id=self.order_id,
            tax_rule_id=self.tax_rule.id,
            subtotal=Decimal('-100.00'),
            tax_amount=Decimal('10.00')
        )
        
        with self.assertRaises(ValidationError):
            calc.clean()
