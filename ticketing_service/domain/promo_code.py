import uuid
from decimal import Decimal
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class PromoCode(models.Model):
    """Promotional code model with business logic."""
    
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=50, unique=True, db_index=True)
    event_id = models.UUIDField(db_index=True, null=True, blank=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    max_uses = models.IntegerField(default=0)
    current_uses = models.IntegerField(default=0)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    min_purchase_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'promo_codes'
        indexes = [
            models.Index(fields=['code', 'is_active']),
            models.Index(fields=['event_id']),
        ]
    
    def __str__(self):
        return f"{self.code} - {self.discount_value}"
    
    def clean(self):
        """Validate promo code business rules."""
        if self.discount_value <= 0:
            raise ValidationError("Discount value must be positive")
        
        if self.discount_type == 'percentage' and self.discount_value > 100:
            raise ValidationError("Percentage discount cannot exceed 100")
        
        if self.max_uses < 0:
            raise ValidationError("Max uses cannot be negative")
        
        if self.valid_until <= self.valid_from:
            raise ValidationError("Valid until must be after valid from")
        
        if self.min_purchase_amount < 0:
            raise ValidationError("Minimum purchase amount cannot be negative")
    
    def is_valid(self) -> bool:
        """Check if promo code is valid for use."""
        now = timezone.now()
        return (
            self.is_active and
            self.valid_from <= now <= self.valid_until and
            (self.max_uses == 0 or self.current_uses < self.max_uses)
        )
    
    def can_apply(self, order_amount: Decimal) -> bool:
        """Check if promo code can be applied to order."""
        return self.is_valid() and order_amount >= self.min_purchase_amount
    
    def calculate_discount(self, amount: Decimal) -> Decimal:
        """Calculate discount amount."""
        if self.discount_type == 'percentage':
            return (amount * self.discount_value / 100).quantize(Decimal('0.01'))
        return min(self.discount_value, amount)
    
    def apply(self) -> None:
        """Apply promo code (increment usage)."""
        if not self.is_valid():
            raise ValidationError("Promo code is not valid")
        
        if self.max_uses > 0 and self.current_uses >= self.max_uses:
            raise ValidationError("Promo code usage limit reached")
        
        self.current_uses += 1
        self.save()
    
    def remaining_uses(self) -> int:
        """Get remaining uses."""
        if self.max_uses == 0:
            return -1  # Unlimited
        return max(0, self.max_uses - self.current_uses)
