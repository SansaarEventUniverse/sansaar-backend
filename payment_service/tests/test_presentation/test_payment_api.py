from decimal import Decimal
from django.test import TestCase
import uuid
import json

from domain.payment import Payment, PaymentMethod


class PaymentAPITest(TestCase):
    """Tests for payment API endpoints."""
    
    def setUp(self):
        self.payment_method = PaymentMethod.objects.create(
            name='Stripe USD',
            gateway='stripe',
            currency='USD'
        )
    
    def test_process_payment(self):
        """Test processing payment endpoint."""
        data = {
            'order_id': str(uuid.uuid4()),
            'payment_method_id': str(self.payment_method.id),
            'amount': '100.00'
        }
        response = self.client.post(
            '/api/payments/process/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['status'], 'pending')
    
    def test_refund_payment(self):
        """Test refund payment endpoint."""
        payment = Payment.objects.create(
            order_id=uuid.uuid4(),
            payment_method=self.payment_method,
            amount=Decimal('100.00'),
            currency='USD',
            status='completed'
        )
        data = {'amount': '50.00', 'reason': 'Customer request'}
        response = self.client.post(
            f'/api/payments/{payment.id}/refund/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'partially_refunded')
    
    def test_get_payment(self):
        """Test get payment endpoint."""
        payment = Payment.objects.create(
            order_id=uuid.uuid4(),
            payment_method=self.payment_method,
            amount=Decimal('100.00'),
            currency='USD'
        )
        response = self.client.get(f'/api/payments/{payment.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['amount'], '100.00')
