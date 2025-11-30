import uuid
from decimal import Decimal
from datetime import timedelta
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Subscription(models.Model):
    """Subscription model for recurring payments."""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ]
    
    BILLING_CYCLE_CHOICES = [
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(db_index=True)
    plan_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    billing_cycle = models.CharField(max_length=20, choices=BILLING_CYCLE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    start_date = models.DateTimeField(default=timezone.now)
    next_billing_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'subscriptions'
        indexes = [
            models.Index(fields=['user_id', 'status']),
            models.Index(fields=['next_billing_date']),
        ]
    
    def __str__(self):
        return f"Subscription {self.plan_name} - {self.user_id}"
    
    def is_active(self) -> bool:
        """Check if subscription is active."""
        return self.status == 'active'
    
    def pause(self) -> None:
        """Pause the subscription."""
        if self.status != 'active':
            raise ValidationError("Can only pause active subscriptions")
        self.status = 'paused'
        self.save()
    
    def cancel(self) -> None:
        """Cancel the subscription."""
        if self.status == 'cancelled':
            raise ValidationError("Subscription already cancelled")
        self.status = 'cancelled'
        self.save()
    
    def calculate_next_billing_date(self) -> None:
        """Calculate next billing date based on cycle."""
        if self.billing_cycle == 'monthly':
            self.next_billing_date = self.next_billing_date + timedelta(days=30)
        elif self.billing_cycle == 'quarterly':
            self.next_billing_date = self.next_billing_date + timedelta(days=90)
        elif self.billing_cycle == 'yearly':
            self.next_billing_date = self.next_billing_date + timedelta(days=365)
        self.save()


class RecurringPayment(models.Model):
    """Recurring payment model for subscription billing."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subscription_id = models.UUIDField(db_index=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    billing_date = models.DateTimeField()
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'recurring_payments'
        indexes = [
            models.Index(fields=['subscription_id', 'status']),
            models.Index(fields=['billing_date']),
        ]
    
    def __str__(self):
        return f"Payment {self.id} - {self.amount}"
    
    def process(self, transaction_id: str) -> None:
        """Mark payment as processed."""
        if self.status != 'pending':
            raise ValidationError("Only pending payments can be processed")
        self.status = 'completed'
        self.transaction_id = transaction_id
        self.processed_at = timezone.now()
        self.save()
    
    def fail(self) -> None:
        """Mark payment as failed."""
        if self.status == 'completed':
            raise ValidationError("Cannot fail completed payment")
        self.status = 'failed'
        self.save()
