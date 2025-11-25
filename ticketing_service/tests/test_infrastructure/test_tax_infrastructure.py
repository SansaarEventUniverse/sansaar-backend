from decimal import Decimal
from django.test import TestCase
import uuid

from domain.tax import TaxRule, TaxCalculation
from infrastructure.repositories.tax_repository import (
    TaxRepository,
    TaxCalculationEngine
)


class TaxRepositoryTest(TestCase):
    """Tests for TaxRepository."""
    
    def setUp(self):
        self.repository = TaxRepository()
        
        TaxRule.objects.create(
            name='US Tax',
            country='US',
            tax_rate=Decimal('10.00')
        )
        
        TaxRule.objects.create(
            name='UK VAT',
            country='UK',
            tax_rate=Decimal('20.00')
        )
    
    def test_get_active_rules(self):
        """Test getting active tax rules."""
        rules = self.repository.get_active_rules()
        self.assertEqual(len(rules), 2)
    
    def test_get_active_rules_by_country(self):
        """Test getting active rules by country."""
        rules = self.repository.get_active_rules('US')
        self.assertEqual(len(rules), 1)
        self.assertEqual(rules[0].country, 'US')


class TaxCalculationEngineTest(TestCase):
    """Tests for TaxCalculationEngine."""
    
    def setUp(self):
        self.tax_rule = TaxRule.objects.create(
            name='Test Tax',
            tax_rate=Decimal('10.00')
        )
    
    def test_calculate_with_rule(self):
        """Test calculating tax with rule."""
        result = TaxCalculationEngine.calculate_with_rule(
            Decimal('100.00'),
            self.tax_rule
        )
        
        self.assertEqual(result['subtotal'], Decimal('100.00'))
        self.assertEqual(result['tax_amount'], Decimal('10.00'))
        self.assertEqual(result['total'], Decimal('110.00'))
    
    def test_calculate_reverse_tax(self):
        """Test calculating reverse tax."""
        result = TaxCalculationEngine.calculate_reverse_tax(
            Decimal('110.00'),
            Decimal('10.00')
        )
        
        self.assertEqual(result['subtotal'], Decimal('100.00'))
        self.assertEqual(result['tax_amount'], Decimal('10.00'))
