from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
import uuid

from domain.promo_code import PromoCode
from domain.order import Order, OrderItem
from domain.ticket_type import TicketType
from application.promo_code_service import (
    CreatePromoCodeService,
    ValidatePromoCodeService,
    ApplyDiscountService
)


class CreatePromoCodeServiceTest(TestCase):
    """Tests for CreatePromoCodeService."""
    
    def setUp(self):
        self.service = CreatePromoCodeService()
        self.now = timezone.now()
    
    def test_create_promo_code(self):
        """Test creating a promo code."""
        data = {
            'code': 'save20',
            'discount_type': 'percentage',
            'discount_value': Decimal('20.00'),
            'max_uses': 100,
            'valid_from': self.now,
            'valid_until': self.now + timedelta(days=30)
        }
        
        promo = self.service.execute(data)
        self.assertEqual(promo.code, 'SAVE20')
        self.assertEqual(promo.discount_value, Decimal('20.00'))


class ValidatePromoCodeServiceTest(TestCase):
    """Tests for ValidatePromoCodeService."""
    
    def setUp(self):
        self.service = ValidatePromoCodeService()
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
    
    def test_validate_promo_code(self):
        """Test validating a promo code."""
        result = self.service.execute('SAVE20', Decimal('100.00'), self.event_id)
        
        self.assertEqual(result['discount_amount'], Decimal('20.00'))
        self.assertEqual(result['final_amount'], Decimal('80.00'))
    
    def test_invalid_promo_code(self):
        """Test invalid promo code."""
        with self.assertRaises(ValidationError):
            self.service.execute('INVALID', Decimal('100.00'))
    
    def test_below_minimum_purchase(self):
        """Test promo code with amount below minimum."""
        with self.assertRaises(ValidationError):
            self.service.execute('SAVE20', Decimal('30.00'), self.event_id)


class ApplyDiscountServiceTest(TestCase):
    """Tests for ApplyDiscountService."""
    
    def setUp(self):
        self.service = ApplyDiscountService()
        self.event_id = uuid.uuid4()
        now = timezone.now()
        
        self.promo = PromoCode.objects.create(
            code='SAVE20',
            event_id=self.event_id,
            discount_type='percentage',
            discount_value=Decimal('20.00'),
            max_uses=100,
            valid_from=now - timedelta(days=1),
            valid_until=now + timedelta(days=30)
        )
        
        self.ticket_type = TicketType.objects.create(
            event_id=self.event_id,
            name='General',
            price=Decimal('50.00'),
            quantity=100,
            sale_start=now - timedelta(days=1),
            sale_end=now + timedelta(days=30)
        )
        
        self.order = Order.objects.create(
            user_id=uuid.uuid4(),
            event_id=self.event_id,
            total_amount=Decimal('100.00')
        )
        OrderItem.objects.create(
            order=self.order,
            ticket_type_id=self.ticket_type.id,
            quantity=2,
            unit_price=Decimal('50.00')
        )
    
    def test_apply_discount(self):
        """Test applying discount to order."""
        order = self.service.execute(self.order.id, 'SAVE20')
        
        self.assertEqual(order.total_amount, Decimal('80.00'))
        
        self.promo.refresh_from_db()
        self.assertEqual(self.promo.current_uses, 1)
    
    def test_apply_to_non_pending_order(self):
        """Test cannot apply to non-pending order."""
        self.order.status = 'confirmed'
        self.order.save()
        
        with self.assertRaises(ValidationError):
            self.service.execute(self.order.id, 'SAVE20')
