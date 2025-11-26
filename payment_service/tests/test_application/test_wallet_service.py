from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
import uuid

from domain.wallet import MobileWallet, WalletTransaction
from application.wallet_service import (
    MobileWalletService,
    WalletPaymentService,
    WalletTopUpService
)


class MobileWalletServiceTest(TestCase):
    """Tests for MobileWalletService."""
    
    def setUp(self):
        self.service = MobileWalletService()
        self.user_id = uuid.uuid4()
    
    def test_create_wallet(self):
        """Test creating a wallet."""
        data = {
            'user_id': self.user_id,
            'wallet_type': 'apple_pay',
            'wallet_token': 'token_123',
            'device_id': 'device_123'
        }
        
        wallet = self.service.create_wallet(data)
        self.assertEqual(wallet.wallet_type, 'apple_pay')
        self.assertTrue(wallet.is_active())
    
    def test_get_wallet(self):
        """Test getting a wallet."""
        wallet = MobileWallet.objects.create(
            user_id=self.user_id,
            wallet_type='google_pay',
            wallet_token='token_456',
            device_id='device_456'
        )
        
        result = self.service.get_wallet(wallet.id)
        self.assertEqual(result.id, wallet.id)


class WalletPaymentServiceTest(TestCase):
    """Tests for WalletPaymentService."""
    
    def setUp(self):
        self.service = WalletPaymentService()
        self.wallet = MobileWallet.objects.create(
            user_id=uuid.uuid4(),
            wallet_type='apple_pay',
            wallet_token='token_123',
            device_id='device_123'
        )
    
    def test_process_payment(self):
        """Test processing wallet payment."""
        data = {
            'wallet_id': self.wallet.id,
            'order_id': uuid.uuid4(),
            'amount': Decimal('100.00')
        }
        
        transaction = self.service.process_payment(data)
        
        self.assertEqual(transaction.status, 'pending')
        self.assertEqual(transaction.amount, Decimal('100.00'))
        
        self.wallet.refresh_from_db()
        self.assertIsNotNone(self.wallet.last_used)
    
    def test_process_payment_inactive_wallet(self):
        """Test cannot process payment with inactive wallet."""
        self.wallet.status = 'inactive'
        self.wallet.save()
        
        data = {
            'wallet_id': self.wallet.id,
            'order_id': uuid.uuid4(),
            'amount': Decimal('100.00')
        }
        
        with self.assertRaises(ValidationError):
            self.service.process_payment(data)


class WalletTopUpServiceTest(TestCase):
    """Tests for WalletTopUpService."""
    
    def setUp(self):
        self.service = WalletTopUpService()
        self.wallet = MobileWallet.objects.create(
            user_id=uuid.uuid4(),
            wallet_type='apple_pay',
            wallet_token='token_123',
            device_id='device_123'
        )
    
    def test_add_to_wallet(self):
        """Test adding ticket to wallet."""
        ticket_id = uuid.uuid4()
        
        result = self.service.add_to_wallet(self.wallet.id, ticket_id)
        
        self.assertEqual(result['status'], 'added')
        self.assertEqual(result['wallet_type'], 'apple_pay')
