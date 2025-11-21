from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
import uuid

from domain.promo_code import PromoCode
from infrastructure.repositories.promo_code_repository import (
    PromoCodeRepository,
    DiscountCalculator
)


class PromoCodeRepositoryTest(TestCase):
    """Tests for PromoCodeRepository."""
    
    def setUp(self):
        self.repository = PromoCodeRepository()
        self.event_id = uuid.uuid4()
        now = timezone.now()
        
        self.promo1 = PromoCode.objects.create(
            code='ACTIVE1',
            event_id=self.event_id,
            discount_type='percentage',
            discount_value=Decimal('20.00'),
            max_uses=100,
            valid_from=now - timedelta(days=1),
            valid_until=now + timedelta(days=30)
        )
        
        self.promo2 = PromoCode.objects.create(
            code='EXPIRED',
            event_id=self.event_id,
            discount_type='percentage',
            discount_value=Decimal('10.00'),
            max_uses=50,
            valid_from=now - timedelta(days=10),
            valid_until=now - timedelta(days=1)
        )
    
    def test_get_active_codes(self):
        """Test getting active promo codes."""
        codes = self.repository.get_active_codes(self.event_id)
        self.assertEqual(len(codes), 1)
        self.assertEqual(codes[0].code, 'ACTIVE1')
    
    def test_get_analytics(self):
        """Test getting promo code analytics."""
        self.promo1.current_uses = 25
        self.promo1.save()
        
        analytics = self.repository.get_analytics(self.promo1.id)
        
        self.assertEqual(analytics['total_uses'], 25)
        self.assertEqual(analytics['remaining_uses'], 75)
        self.assertEqual(analytics['usage_rate'], 25.0)


class DiscountCalculatorTest(TestCase):
    """Tests for DiscountCalculator."""
    
    def test_percentage_discount(self):
        """Test percentage discount calculation."""
        discount = DiscountCalculator.calculate_percentage_discount(
            Decimal('100.00'),
            Decimal('20.00')
        )
        self.assertEqual(discount, Decimal('20.00'))
    
    def test_fixed_discount(self):
        """Test fixed discount calculation."""
        discount = DiscountCalculator.calculate_fixed_discount(
            Decimal('100.00'),
            Decimal('15.00')
        )
        self.assertEqual(discount, Decimal('15.00'))
    
    def test_apply_percentage_discount(self):
        """Test applying percentage discount."""
        final = DiscountCalculator.apply_discount(
            Decimal('100.00'),
            'percentage',
            Decimal('20.00')
        )
        self.assertEqual(final, Decimal('80.00'))
    
    def test_apply_fixed_discount(self):
        """Test applying fixed discount."""
        final = DiscountCalculator.apply_discount(
            Decimal('100.00'),
            'fixed',
            Decimal('15.00')
        )
        self.assertEqual(final, Decimal('85.00'))
