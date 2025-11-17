from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
import uuid

from domain.payment import Payment, PaymentMethod
from application.payment_service import (
    ProcessPaymentService,
    RefundPaymentService,
    PaymentValidationService
)


class ProcessPaymentServiceTest(TestCase):
    """Tests for ProcessPaymentService."""
    
    def setUp(self):
        self.service = ProcessPaymentService()
        self.payment_method = PaymentMethod.objects.create(
            name='Stripe USD',
            gateway='stripe',
            currency='USD'
        )
    
    def test_process_payment(self):
        """Test processing a payment."""
        data = {
            'order_id': uuid.uuid4(),
            'payment_method_id': self.payment_method.id,
            'amount': Decimal('100.00')
        }
        payment = self.service.execute(data)
        self.assertEqual(payment.amount, Decimal('100.00'))
        self.assertEqual(payment.status, 'pending')
    
    def test_process_payment_invalid_method(self):
        """Test processing with invalid payment method."""
        data = {
            'order_id': uuid.uuid4(),
            'payment_method_id': uuid.uuid4(),
            'amount': Decimal('100.00')
        }
        with self.assertRaises(ValidationError):
            self.service.execute(data)


class RefundPaymentServiceTest(TestCase):
    """Tests for RefundPaymentService."""
    
    def setUp(self):
        self.service = RefundPaymentService()
        payment_method = PaymentMethod.objects.create(
            name='Stripe USD',
            gateway='stripe',
            currency='USD'
        )
        self.payment = Payment.objects.create(
            order_id=uuid.uuid4(),
            payment_method=payment_method,
            amount=Decimal('100.00'),
            currency='USD',
            status='completed'
        )
    
    def test_refund_payment(self):
        """Test refunding a payment."""
        result = self.service.execute(self.payment.id, Decimal('50.00'), 'Customer request')
        self.assertEqual(result.refund_amount, Decimal('50.00'))
        self.assertEqual(result.status, 'partially_refunded')
    
    def test_refund_nonexistent_payment(self):
        """Test refunding non-existent payment."""
        with self.assertRaises(ValidationError):
            self.service.execute(uuid.uuid4(), Decimal('50.00'))


class PaymentValidationServiceTest(TestCase):
    """Tests for PaymentValidationService."""
    
    def setUp(self):
        self.service = PaymentValidationService()
    
    def test_validate_payment_data(self):
        """Test validating payment data."""
        data = {
            'order_id': uuid.uuid4(),
            'payment_method_id': uuid.uuid4(),
            'amount': Decimal('100.00')
        }
        result = self.service.validate_payment_data(data)
        self.assertEqual(result, data)
    
    def test_validate_missing_fields(self):
        """Test validation with missing fields."""
        data = {}
        with self.assertRaises(ValidationError):
            self.service.validate_payment_data(data)
