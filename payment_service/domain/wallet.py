import uuid
from decimal import Decimal
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class MobileWallet(models.Model):
    """Mobile wallet model for digital payments."""
    
    WALLET_TYPE_CHOICES = [
        ('apple_pay', 'Apple Pay'),
        ('google_pay', 'Google Pay'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(db_index=True)
    wallet_type = models.CharField(max_length=20, choices=WALLET_TYPE_CHOICES)
    wallet_token = models.CharField(max_length=255, unique=True)
    device_id = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    last_used = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'mobile_wallets'
        indexes = [
            models.Index(fields=['user_id', 'status']),
        ]
    
    def __str__(self):
        return f"{self.wallet_type} - {self.user_id}"
    
    def is_active(self) -> bool:
        """Check if wallet is active."""
        return self.status == 'active'
    
    def update_last_used(self) -> None:
        """Update last used timestamp."""
        self.last_used = timezone.now()
        self.save()
    
    def suspend(self) -> None:
        """Suspend the wallet."""
        if self.status == 'suspended':
            raise ValidationError("Wallet is already suspended")
        self.status = 'suspended'
        self.save()


class WalletTransaction(models.Model):
    """Wallet transaction model."""
    
    TRANSACTION_TYPE_CHOICES = [
        ('payment', 'Payment'),
        ('refund', 'Refund'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wallet_id = models.UUIDField(db_index=True)
    order_id = models.UUIDField(db_index=True)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    gateway_transaction_id = models.CharField(max_length=255, blank=True)
    gateway_response = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'wallet_transactions'
        indexes = [
            models.Index(fields=['wallet_id']),
            models.Index(fields=['order_id']),
        ]
    
    def __str__(self):
        return f"Transaction {self.id} - {self.amount}"
    
    def clean(self):
        """Validate transaction."""
        if self.amount <= 0:
            raise ValidationError("Amount must be positive")
    
    def complete(self, transaction_id: str) -> None:
        """Mark transaction as completed."""
        if self.status != 'pending':
            raise ValidationError("Only pending transactions can be completed")
        self.status = 'completed'
        self.gateway_transaction_id = transaction_id
        self.completed_at = timezone.now()
        self.save()
    
    def fail(self) -> None:
        """Mark transaction as failed."""
        if self.status == 'completed':
            raise ValidationError("Cannot fail completed transaction")
        self.status = 'failed'
        self.save()
