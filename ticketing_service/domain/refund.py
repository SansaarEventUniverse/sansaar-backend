import uuid
from decimal import Decimal
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class RefundPolicy(models.Model):
    """Refund policy model for events."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_id = models.UUIDField(db_index=True)
    refund_allowed = models.BooleanField(default=True)
    refund_before_hours = models.IntegerField(default=24)
    refund_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('100.00'))
    processing_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'refund_policies'
    
    def __str__(self):
        return f"Policy for {self.event_id}"
    
    def clean(self):
        """Validate refund policy."""
        if self.refund_percentage < 0 or self.refund_percentage > 100:
            raise ValidationError("Refund percentage must be between 0 and 100")
        
        if self.processing_fee < 0:
            raise ValidationError("Processing fee cannot be negative")
        
        if self.refund_before_hours < 0:
            raise ValidationError("Refund before hours cannot be negative")


class Refund(models.Model):
    """Refund model for ticket cancellations."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket_id = models.UUIDField(db_index=True)
    order_id = models.UUIDField(db_index=True)
    payment_id = models.UUIDField(null=True, blank=True)
    original_amount = models.DecimalField(max_digits=10, decimal_places=2)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2)
    processing_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    rejected_reason = models.TextField(blank=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'refunds'
        indexes = [
            models.Index(fields=['ticket_id']),
            models.Index(fields=['order_id']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Refund {self.id} - {self.refund_amount}"
    
    def clean(self):
        """Validate refund."""
        if self.original_amount < 0:
            raise ValidationError("Original amount cannot be negative")
        
        if self.refund_amount < 0:
            raise ValidationError("Refund amount cannot be negative")
        
        if self.refund_amount > self.original_amount:
            raise ValidationError("Refund amount cannot exceed original amount")
        
        if self.processing_fee < 0:
            raise ValidationError("Processing fee cannot be negative")
    
    def calculate_refund(self, policy: RefundPolicy) -> Decimal:
        """Calculate refund amount based on policy."""
        refund = (self.original_amount * policy.refund_percentage / 100) - policy.processing_fee
        return max(Decimal('0.00'), refund).quantize(Decimal('0.01'))
    
    def process(self) -> None:
        """Mark refund as processing."""
        if self.status != 'pending':
            raise ValidationError("Only pending refunds can be processed")
        self.status = 'processing'
        self.save()
    
    def complete(self) -> None:
        """Mark refund as completed."""
        if self.status != 'processing':
            raise ValidationError("Only processing refunds can be completed")
        self.status = 'completed'
        self.processed_at = timezone.now()
        self.save()
    
    def reject(self, reason: str) -> None:
        """Reject refund."""
        if self.status not in ['pending', 'processing']:
            raise ValidationError("Cannot reject completed or already rejected refund")
        self.status = 'rejected'
        self.rejected_reason = reason
        self.save()
