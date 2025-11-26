import uuid
from decimal import Decimal
from typing import Dict, Any
from django.core.exceptions import ValidationError

from domain.wallet import MobileWallet, WalletTransaction


class MobileWalletService:
    """Service for managing mobile wallets."""
    
    def create_wallet(self, data: Dict[str, Any]) -> MobileWallet:
        """Create a new mobile wallet."""
        wallet = MobileWallet.objects.create(
            user_id=data['user_id'],
            wallet_type=data['wallet_type'],
            wallet_token=data['wallet_token'],
            device_id=data['device_id']
        )
        return wallet
    
    def get_wallet(self, wallet_id: uuid.UUID) -> MobileWallet:
        """Get wallet by ID."""
        try:
            return MobileWallet.objects.get(id=wallet_id)
        except MobileWallet.DoesNotExist:
            raise ValidationError("Wallet not found")


class WalletPaymentService:
    """Service for processing wallet payments."""
    
    def process_payment(self, data: Dict[str, Any]) -> WalletTransaction:
        """Process a wallet payment."""
        try:
            wallet = MobileWallet.objects.get(id=data['wallet_id'])
        except MobileWallet.DoesNotExist:
            raise ValidationError("Wallet not found")
        
        if not wallet.is_active():
            raise ValidationError("Wallet is not active")
        
        transaction = WalletTransaction.objects.create(
            wallet_id=wallet.id,
            order_id=data['order_id'],
            transaction_type='payment',
            amount=data['amount'],
            currency=data.get('currency', 'USD')
        )
        
        wallet.update_last_used()
        
        return transaction


class WalletTopUpService:
    """Service for wallet top-up operations."""
    
    def add_to_wallet(self, wallet_id: uuid.UUID, ticket_id: uuid.UUID) -> Dict[str, Any]:
        """Add ticket to mobile wallet."""
        try:
            wallet = MobileWallet.objects.get(id=wallet_id)
        except MobileWallet.DoesNotExist:
            raise ValidationError("Wallet not found")
        
        if not wallet.is_active():
            raise ValidationError("Wallet is not active")
        
        # Generate wallet pass data
        pass_data = {
            'wallet_id': str(wallet.id),
            'ticket_id': str(ticket_id),
            'wallet_type': wallet.wallet_type,
            'status': 'added'
        }
        
        wallet.update_last_used()
        
        return pass_data
