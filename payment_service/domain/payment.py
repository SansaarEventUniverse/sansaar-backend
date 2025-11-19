import uuid
from decimal import Decimal
from django.db import models
from django.core.exceptions import ValidationError


class PaymentMethod(models.Model):
    """Payment method/gateway abstraction."""
    
    GATEWAY_CHOICES = [
        ('stripe', 'Stripe'),
        ('paypal', 'PayPal'),
        ('esewa', 'eSewa'),
        ('khalti', 'Khalti'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    gateway = models.CharField(max_length=20, choices=GATEWAY_CHOICES)
    currency = models.CharField(max_length=3)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'payment_methods'
    
    def __str__(self):
        return f"{self.name} ({self.gateway})"


class Payment(models.Model):
    """Payment model with business logic."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
        ('partially_refunded', 'Partially Refunded'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_id = models.UUIDField(db_index=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    gateway_transaction_id = models.CharField(max_length=255, blank=True)
    gateway_response = models.JSONField(default=dict)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    refund_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'payments'
        indexes = [
            models.Index(fields=['order_id', 'status']),
            models.Index(fields=['gateway_transaction_id']),
        ]
    
    def __str__(self):
        return f"Payment {self.id} - {self.amount} {self.currency}"
    
    def clean(self):
        """Validate payment business rules."""
        if self.amount <= 0:
            raise ValidationError("Amount must be positive")
        
        if self.refund_amount < 0:
            raise ValidationError("Refund amount cannot be negative")
        
        if self.refund_amount > self.amount:
            raise ValidationError("Refund amount cannot exceed payment amount")
    
    def can_refund(self) -> bool:
        """Check if payment can be refunded."""
        return self.status in ['completed', 'partially_refunded'] and self.refund_amount < self.amount
    
    def process(self, transaction_id: str, response: dict) -> None:
        """Mark payment as processing."""
        self.status = 'processing'
        self.gateway_transaction_id = transaction_id
        self.gateway_response = response
        self.save()
    
    def complete(self) -> None:
        """Mark payment as completed."""
        if self.status != 'processing':
            raise ValidationError("Only processing payments can be completed")
        self.status = 'completed'
        self.save()
    
    def fail(self, reason: str = '') -> None:
        """Mark payment as failed."""
        self.status = 'failed'
        if reason:
            self.gateway_response['error'] = reason
        self.save()
    
    def refund(self, amount: Decimal, reason: str = '') -> None:
        """Process refund."""
        if not self.can_refund():
            raise ValidationError("Payment cannot be refunded")
        
        if amount <= 0 or amount > (self.amount - self.refund_amount):
            raise ValidationError("Invalid refund amount")
        
        self.refund_amount += amount
        self.refund_reason = reason
        
        if self.refund_amount >= self.amount:
            self.status = 'refunded'
        else:
            self.status = 'partially_refunded'
        
        self.save()
