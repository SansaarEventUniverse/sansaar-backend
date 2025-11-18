from decimal import Decimal
from django.test import TestCase
from unittest.mock import patch, MagicMock

from infrastructure.services.stripe_client import StripeClient


class StripeClientTest(TestCase):
    """Tests for StripeClient."""
    
    def setUp(self):
        self.client = StripeClient()
    
    @patch('infrastructure.services.stripe_client.stripe.PaymentIntent.create')
    def test_create_payment_intent(self, mock_create):
        """Test creating payment intent."""
        mock_create.return_value = MagicMock(
            id='pi_123',
            status='requires_payment_method',
            client_secret='secret_123'
        )
        
        result = self.client.create_payment_intent(
            Decimal('100.00'),
            'USD',
            {'order_id': 'order_123'}
        )
        
        self.assertTrue(result['success'])
        self.assertEqual(result['transaction_id'], 'pi_123')
    
    @patch('infrastructure.services.stripe_client.stripe.Refund.create')
    def test_refund_payment(self, mock_refund):
        """Test refunding payment."""
        mock_refund.return_value = MagicMock(
            id='re_123',
            status='succeeded'
        )
        
        result = self.client.refund_payment('pi_123', Decimal('50.00'))
        
        self.assertTrue(result['success'])
        self.assertEqual(result['refund_id'], 're_123')
