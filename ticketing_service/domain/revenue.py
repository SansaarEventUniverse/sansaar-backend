import uuid
from decimal import Decimal
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Revenue(models.Model):
    """Revenue model for tracking event revenue."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_id = models.UUIDField(db_index=True)
    order_id = models.UUIDField(db_index=True)
    gross_amount = models.DecimalField(max_digits=10, decimal_places=2)
    platform_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    payment_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    net_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'revenues'
        indexes = [
            models.Index(fields=['event_id', 'created_at']),
        ]
    
    def __str__(self):
        return f"Revenue {self.id} - {self.net_amount}"
    
    def clean(self):
        """Validate revenue."""
        if self.gross_amount < 0:
            raise ValidationError("Gross amount cannot be negative")
        
        if self.platform_fee < 0:
            raise ValidationError("Platform fee cannot be negative")
        
        if self.payment_fee < 0:
            raise ValidationError("Payment fee cannot be negative")
    
    def calculate_net(self) -> Decimal:
        """Calculate net amount."""
        return self.gross_amount - self.platform_fee - self.payment_fee
    
    def save(self, *args, **kwargs):
        """Calculate net amount before saving."""
        self.net_amount = self.calculate_net()
        super().save(*args, **kwargs)


class RevenueReport(models.Model):
    """Revenue report model for analytics."""
    
    PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('custom', 'Custom'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_id = models.UUIDField(db_index=True)
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    total_gross = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_fees = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_net = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_orders = models.IntegerField(default=0)
    total_refunds = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'revenue_reports'
        indexes = [
            models.Index(fields=['event_id', 'period']),
        ]
    
    def __str__(self):
        return f"Report {self.event_id} - {self.period}"
    
    def clean(self):
        """Validate report."""
        if self.end_date <= self.start_date:
            raise ValidationError("End date must be after start date")
