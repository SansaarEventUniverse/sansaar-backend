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


class PaymentWorkflowIntegrationTest(TestCase):
    """Integration tests for payment workflows."""
    
    def setUp(self):
        self.payment_method = PaymentMethod.objects.create(
            name='Stripe',
            gateway='stripe',
            is_active=True
        )
    
    def test_complete_payment_workflow(self):
        """Test complete payment from creation to completion."""
        # Create payment
        service = ProcessPaymentService()
        payment = service.execute({
            'order_id': uuid.uuid4(),
            'payment_method_id': self.payment_method.id,
            'amount': Decimal('100.00'),
            'currency': 'USD'
        })
        
        self.assertEqual(payment.status, 'pending')
        self.assertEqual(payment.amount, Decimal('100.00'))
        
        # Process and complete
        payment.process('txn_pending', {})
        payment.complete()
        
        self.assertEqual(payment.status, 'completed')
    
    def test_payment_refund_workflow(self):
        """Test payment refund workflow."""
        # Create completed payment
        payment = Payment.objects.create(
            order_id=uuid.uuid4(),
            payment_method=self.payment_method,
            amount=Decimal('100.00'),
            currency='USD',
            status='completed',
            gateway_transaction_id='txn_123'
        )
        
        # Partial refund
        payment.refund(Decimal('50.00'), 'Customer request')
        payment.refresh_from_db()
        self.assertEqual(payment.status, 'partially_refunded')
        self.assertEqual(payment.refund_amount, Decimal('50.00'))
        
        # Full refund
        payment.refund(Decimal('50.00'), 'Full refund')
        payment.refresh_from_db()
        self.assertEqual(payment.status, 'refunded')
        self.assertEqual(payment.refund_amount, Decimal('100.00'))
    
    def test_payment_validation(self):
        """Test payment validation."""
        service = PaymentValidationService()
        
        # Valid payment
        result = service.validate_payment_data({
            'order_id': uuid.uuid4(),
            'payment_method_id': self.payment_method.id,
            'amount': Decimal('100.00'),
            'currency': 'USD'
        })
        self.assertIsNotNone(result)
        
        # Invalid amount
        with self.assertRaises(ValidationError):
            service.validate_payment_data({
                'order_id': uuid.uuid4(),
                'payment_method_id': self.payment_method.id,
                'amount': Decimal('-10.00'),
                'currency': 'USD'
            })


class PaymentSecurityTest(TestCase):
    """Security tests for payment system."""
    
    def setUp(self):
        self.payment_method = PaymentMethod.objects.create(
            name='Stripe',
            gateway='stripe',
            is_active=True
        )
    
    def test_negative_amount_prevention(self):
        """Test that negative amounts are prevented."""
        payment = Payment(
            order_id=uuid.uuid4(),
            payment_method=self.payment_method,
            amount=Decimal('-100.00'),
            currency='USD'
        )
        
        with self.assertRaises(ValidationError):
            payment.clean()
    
    def test_excessive_refund_prevention(self):
        """Test that refunds cannot exceed payment amount."""
        payment = Payment.objects.create(
            order_id=uuid.uuid4(),
            payment_method=self.payment_method,
            amount=Decimal('100.00'),
            currency='USD',
            status='completed'
        )
        
        with self.assertRaises(ValidationError):
            payment.refund(Decimal('150.00'), 'Invalid refund')
    
    def test_refund_non_completed_payment(self):
        """Test that non-completed payments cannot be refunded."""
        payment = Payment.objects.create(
            order_id=uuid.uuid4(),
            payment_method=self.payment_method,
            amount=Decimal('100.00'),
            currency='USD',
            status='pending'
        )
        
        self.assertFalse(payment.can_refund())
