from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
import uuid

from domain.promo_code import PromoCode


class PromoCodeModelTest(TestCase):
    """Tests for PromoCode model."""
    
    def setUp(self):
        self.event_id = uuid.uuid4()
        now = timezone.now()
        
        self.promo = PromoCode.objects.create(
            code='SAVE20',
            event_id=self.event_id,
            discount_type='percentage',
            discount_value=Decimal('20.00'),
            max_uses=100,
            valid_from=now - timedelta(days=1),
            valid_until=now + timedelta(days=30),
            min_purchase_amount=Decimal('50.00')
        )
    
    def test_create_promo_code(self):
        """Test creating a promo code."""
        self.assertEqual(self.promo.code, 'SAVE20')
        self.assertEqual(self.promo.discount_value, Decimal('20.00'))
        self.assertEqual(self.promo.current_uses, 0)
    
    def test_percentage_discount_calculation(self):
        """Test percentage discount calculation."""
        discount = self.promo.calculate_discount(Decimal('100.00'))
        self.assertEqual(discount, Decimal('20.00'))
    
    def test_fixed_discount_calculation(self):
        """Test fixed discount calculation."""
        now = timezone.now()
        promo = PromoCode.objects.create(
            code='FIXED10',
            discount_type='fixed',
            discount_value=Decimal('10.00'),
            max_uses=0,
            valid_from=now - timedelta(days=1),
            valid_until=now + timedelta(days=30)
        )
        
        discount = promo.calculate_discount(Decimal('100.00'))
        self.assertEqual(discount, Decimal('10.00'))
    
    def test_promo_code_validation(self):
        """Test promo code is valid."""
        self.assertTrue(self.promo.is_valid())
    
    def test_expired_promo_code(self):
        """Test expired promo code is invalid."""
        now = timezone.now()
        promo = PromoCode.objects.create(
            code='EXPIRED',
            discount_type='percentage',
            discount_value=Decimal('10.00'),
            max_uses=0,
            valid_from=now - timedelta(days=10),
            valid_until=now - timedelta(days=1)
        )
        
        self.assertFalse(promo.is_valid())
    
    def test_can_apply_with_min_purchase(self):
        """Test can apply with minimum purchase amount."""
        self.assertTrue(self.promo.can_apply(Decimal('100.00')))
        self.assertFalse(self.promo.can_apply(Decimal('30.00')))
    
    def test_apply_promo_code(self):
        """Test applying promo code increments usage."""
        self.promo.apply()
        self.assertEqual(self.promo.current_uses, 1)
    
    def test_usage_limit(self):
        """Test usage limit enforcement."""
        self.promo.current_uses = 100
        self.promo.save()
        
        with self.assertRaises(ValidationError):
            self.promo.apply()
    
    def test_remaining_uses(self):
        """Test remaining uses calculation."""
        self.assertEqual(self.promo.remaining_uses(), 100)
        self.promo.current_uses = 50
        self.promo.save()
        self.assertEqual(self.promo.remaining_uses(), 50)
    
    def test_invalid_percentage_validation(self):
        """Test percentage over 100 is invalid."""
        promo = PromoCode(
            code='INVALID',
            discount_type='percentage',
            discount_value=Decimal('150.00'),
            max_uses=0,
            valid_from=timezone.now(),
            valid_until=timezone.now() + timedelta(days=1)
        )
        
        with self.assertRaises(ValidationError):
            promo.clean()
