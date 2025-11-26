from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient
import uuid

from domain.wallet import MobileWallet


class WalletPaymentAPITest(TestCase):
    """Tests for wallet payment API."""
    
    def setUp(self):
        self.client = APIClient()
        self.wallet = MobileWallet.objects.create(
            user_id=uuid.uuid4(),
            wallet_type='apple_pay',
            wallet_token='token_123',
            device_id='device_123'
        )
    
    def test_process_wallet_payment(self):
        """Test processing wallet payment."""
        data = {
            'wallet_id': str(self.wallet.id),
            'order_id': str(uuid.uuid4()),
            'amount': '100.00',
            'currency': 'USD'
        }
        
        response = self.client.post('/api/payments/wallet/', data, format='json')
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('transaction_id', response.data)
        self.assertEqual(response.data['status'], 'completed')


class AddToWalletAPITest(TestCase):
    """Tests for add to wallet API."""
    
    def setUp(self):
        self.client = APIClient()
        self.wallet = MobileWallet.objects.create(
            user_id=uuid.uuid4(),
            wallet_type='google_pay',
            wallet_token='token_456',
            device_id='device_456'
        )
    
    def test_add_ticket_to_wallet(self):
        """Test adding ticket to wallet."""
        ticket_id = uuid.uuid4()
        data = {'wallet_id': str(self.wallet.id)}
        
        response = self.client.post(
            f'/api/payments/tickets/{ticket_id}/add-to-wallet/',
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'added')
        self.assertIn('pass_url', response.data)


class WalletStatusAPITest(TestCase):
    """Tests for wallet status API."""
    
    def setUp(self):
        self.client = APIClient()
        self.wallet = MobileWallet.objects.create(
            user_id=uuid.uuid4(),
            wallet_type='apple_pay',
            wallet_token='token_789',
            device_id='device_789'
        )
    
    def test_get_wallet_status(self):
        """Test getting wallet status."""
        response = self.client.get(f'/api/payments/wallets/{self.wallet.id}/status/')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'active')
        self.assertEqual(response.data['wallet_type'], 'apple_pay')
