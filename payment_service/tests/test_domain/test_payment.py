from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
import uuid

from domain.payment import Payment, PaymentMethod


class PaymentMethodModelTest(TestCase):
    """Tests for PaymentMethod model."""
    
    def test_create_payment_method(self):
        """Test creating a payment method."""
        method = PaymentMethod.objects.create(
            name='Stripe USD',
            gateway='stripe',
            currency='USD'
        )
        self.assertEqual(method.name, 'Stripe USD')
        self.assertEqual(method.gateway, 'stripe')
        self.assertTrue(method.is_active)


class PaymentModelTest(TestCase):
    """Tests for Payment model."""
    
    def setUp(self):
        self.payment_method = PaymentMethod.objects.create(
            name='Stripe USD',
            gateway='stripe',
            currency='USD'
        )
        self.order_id = uuid.uuid4()
    
    def test_create_payment(self):
        """Test creating a payment."""
        payment = Payment.objects.create(
            order_id=self.order_id,
            payment_method=self.payment_method,
            amount=Decimal('100.00'),
            currency='USD'
        )
        self.assertEqual(payment.amount, Decimal('100.00'))
        self.assertEqual(payment.status, 'pending')
    
    def test_negative_amount_validation(self):
        """Test that negative amount raises validation error."""
        payment = Payment(
            order_id=self.order_id,
            payment_method=self.payment_method,
            amount=Decimal('-10.00'),
            currency='USD'
        )
        with self.assertRaises(ValidationError):
            payment.clean()
    
    def test_refund_exceeds_amount(self):
        """Test that refund cannot exceed payment amount."""
        payment = Payment(
            order_id=self.order_id,
            payment_method=self.payment_method,
            amount=Decimal('100.00'),
            currency='USD',
            refund_amount=Decimal('150.00')
        )
        with self.assertRaises(ValidationError):
            payment.clean()
    
    def test_can_refund(self):
        """Test can_refund method."""
        payment = Payment.objects.create(
            order_id=self.order_id,
            payment_method=self.payment_method,
            amount=Decimal('100.00'),
            currency='USD',
            status='completed'
        )
        self.assertTrue(payment.can_refund())
    
    def test_cannot_refund_pending(self):
        """Test cannot refund pending payment."""
        payment = Payment.objects.create(
            order_id=self.order_id,
            payment_method=self.payment_method,
            amount=Decimal('100.00'),
            currency='USD',
            status='pending'
        )
        self.assertFalse(payment.can_refund())
    
    def test_process_payment(self):
        """Test processing a payment."""
        payment = Payment.objects.create(
            order_id=self.order_id,
            payment_method=self.payment_method,
            amount=Decimal('100.00'),
            currency='USD'
        )
        payment.process('txn_123', {'status': 'processing'})
        self.assertEqual(payment.status, 'processing')
        self.assertEqual(payment.gateway_transaction_id, 'txn_123')
    
    def test_complete_payment(self):
        """Test completing a payment."""
        payment = Payment.objects.create(
            order_id=self.order_id,
            payment_method=self.payment_method,
            amount=Decimal('100.00'),
            currency='USD',
            status='processing'
        )
        payment.complete()
        self.assertEqual(payment.status, 'completed')
    
    def test_fail_payment(self):
        """Test failing a payment."""
        payment = Payment.objects.create(
            order_id=self.order_id,
            payment_method=self.payment_method,
            amount=Decimal('100.00'),
            currency='USD'
        )
        payment.fail('Insufficient funds')
        self.assertEqual(payment.status, 'failed')
    
    def test_refund_payment(self):
        """Test refunding a payment."""
        payment = Payment.objects.create(
            order_id=self.order_id,
            payment_method=self.payment_method,
            amount=Decimal('100.00'),
            currency='USD',
            status='completed'
        )
        payment.refund(Decimal('50.00'), 'Customer request')
        self.assertEqual(payment.refund_amount, Decimal('50.00'))
        self.assertEqual(payment.status, 'partially_refunded')
    
    def test_full_refund(self):
        """Test full refund changes status."""
        payment = Payment.objects.create(
            order_id=self.order_id,
            payment_method=self.payment_method,
            amount=Decimal('100.00'),
            currency='USD',
            status='completed'
        )
        payment.refund(Decimal('100.00'), 'Full refund')
        self.assertEqual(payment.status, 'refunded')
