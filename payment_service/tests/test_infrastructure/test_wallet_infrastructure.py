from decimal import Decimal
from django.test import TestCase
import uuid

from infrastructure.services.wallet_client import (
    ApplePayClient,
    GooglePayClient,
    WalletPaymentPipeline
)


class ApplePayClientTest(TestCase):
    """Tests for ApplePayClient."""
    
    def setUp(self):
        self.client = ApplePayClient()
    
    def test_process_payment(self):
        """Test processing Apple Pay payment."""
        data = {
            'amount': Decimal('100.00'),
            'currency': 'USD'
        }
        
        result = self.client.process_payment(data)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['status'], 'completed')
        self.assertIn('apple_pay_', result['transaction_id'])
    
    def test_generate_pass(self):
        """Test generating Apple Wallet pass."""
        ticket_data = {'ticket_id': str(uuid.uuid4())}
        
        result = self.client.generate_pass(ticket_data)
        
        self.assertEqual(result['pass_type'], 'apple_wallet')
        self.assertIn('wallet.apple.com', result['pass_url'])


class GooglePayClientTest(TestCase):
    """Tests for GooglePayClient."""
    
    def setUp(self):
        self.client = GooglePayClient()
    
    def test_process_payment(self):
        """Test processing Google Pay payment."""
        data = {
            'amount': Decimal('50.00'),
            'currency': 'USD'
        }
        
        result = self.client.process_payment(data)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['status'], 'completed')
        self.assertIn('google_pay_', result['transaction_id'])
    
    def test_generate_pass(self):
        """Test generating Google Wallet pass."""
        ticket_data = {'ticket_id': str(uuid.uuid4())}
        
        result = self.client.generate_pass(ticket_data)
        
        self.assertEqual(result['pass_type'], 'google_wallet')
        self.assertIn('pay.google.com', result['pass_url'])


class WalletPaymentPipelineTest(TestCase):
    """Tests for WalletPaymentPipeline."""
    
    def setUp(self):
        self.pipeline = WalletPaymentPipeline()
    
    def test_process_apple_pay(self):
        """Test processing through Apple Pay."""
        data = {'amount': Decimal('75.00')}
        
        result = self.pipeline.process('apple_pay', data)
        
        self.assertTrue(result['success'])
        self.assertIn('apple_pay_', result['transaction_id'])
    
    def test_process_google_pay(self):
        """Test processing through Google Pay."""
        data = {'amount': Decimal('60.00')}
        
        result = self.pipeline.process('google_pay', data)
        
        self.assertTrue(result['success'])
        self.assertIn('google_pay_', result['transaction_id'])
    
    def test_unsupported_wallet_type(self):
        """Test unsupported wallet type."""
        data = {'amount': Decimal('100.00')}
        
        with self.assertRaises(ValueError):
            self.pipeline.process('samsung_pay', data)
