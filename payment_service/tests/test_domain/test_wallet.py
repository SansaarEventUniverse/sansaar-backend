from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
import uuid

from domain.wallet import MobileWallet, WalletTransaction


class MobileWalletModelTest(TestCase):
    """Tests for MobileWallet model."""
    
    def setUp(self):
        self.user_id = uuid.uuid4()
    
    def test_create_mobile_wallet(self):
        """Test creating a mobile wallet."""
        wallet = MobileWallet.objects.create(
            user_id=self.user_id,
            wallet_type='apple_pay',
            wallet_token='test_token_123',
            device_id='device_123'
        )
        
        self.assertEqual(wallet.status, 'active')
        self.assertTrue(wallet.is_active())
    
    def test_update_last_used(self):
        """Test updating last used timestamp."""
        wallet = MobileWallet.objects.create(
            user_id=self.user_id,
            wallet_type='google_pay',
            wallet_token='test_token_456',
            device_id='device_456'
        )
        
        wallet.update_last_used()
        self.assertIsNotNone(wallet.last_used)
    
    def test_suspend_wallet(self):
        """Test suspending a wallet."""
        wallet = MobileWallet.objects.create(
            user_id=self.user_id,
            wallet_type='apple_pay',
            wallet_token='test_token_789',
            device_id='device_789'
        )
        
        wallet.suspend()
        self.assertEqual(wallet.status, 'suspended')
        self.assertFalse(wallet.is_active())


class WalletTransactionModelTest(TestCase):
    """Tests for WalletTransaction model."""
    
    def setUp(self):
        self.wallet_id = uuid.uuid4()
        self.order_id = uuid.uuid4()
    
    def test_create_transaction(self):
        """Test creating a wallet transaction."""
        transaction = WalletTransaction.objects.create(
            wallet_id=self.wallet_id,
            order_id=self.order_id,
            transaction_type='payment',
            amount=Decimal('100.00')
        )
        
        self.assertEqual(transaction.status, 'pending')
        self.assertEqual(transaction.amount, Decimal('100.00'))
    
    def test_complete_transaction(self):
        """Test completing a transaction."""
        transaction = WalletTransaction.objects.create(
            wallet_id=self.wallet_id,
            order_id=self.order_id,
            transaction_type='payment',
            amount=Decimal('50.00')
        )
        
        transaction.complete('txn_123')
        self.assertEqual(transaction.status, 'completed')
        self.assertEqual(transaction.gateway_transaction_id, 'txn_123')
        self.assertIsNotNone(transaction.completed_at)
    
    def test_fail_transaction(self):
        """Test failing a transaction."""
        transaction = WalletTransaction.objects.create(
            wallet_id=self.wallet_id,
            order_id=self.order_id,
            transaction_type='payment',
            amount=Decimal('75.00')
        )
        
        transaction.fail()
        self.assertEqual(transaction.status, 'failed')
    
    def test_negative_amount_validation(self):
        """Test negative amount validation."""
        transaction = WalletTransaction(
            wallet_id=self.wallet_id,
            order_id=self.order_id,
            transaction_type='payment',
            amount=Decimal('-10.00')
        )
        
        with self.assertRaises(ValidationError):
            transaction.clean()
