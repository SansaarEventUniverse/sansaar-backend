import uuid
from decimal import Decimal
from django.db import models
from django.core.exceptions import ValidationError


class GroupBooking(models.Model):
    """Group booking model for bulk ticket purchases."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_id = models.UUIDField(db_index=True)
    organizer_id = models.UUIDField(db_index=True)
    group_name = models.CharField(max_length=255)
    min_participants = models.IntegerField()
    max_participants = models.IntegerField()
    current_participants = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'group_bookings'
        indexes = [
            models.Index(fields=['event_id', 'status']),
        ]
    
    def __str__(self):
        return f"Group {self.group_name}"
    
    def can_join(self) -> bool:
        """Check if group can accept more participants."""
        return self.status in ['pending', 'active'] and self.current_participants < self.max_participants
    
    def add_participant(self) -> None:
        """Add a participant to the group."""
        if not self.can_join():
            raise ValidationError("Cannot join this group")
        self.current_participants += 1
        if self.current_participants >= self.min_participants:
            self.status = 'active'
        self.save()
    
    def is_complete(self) -> bool:
        """Check if group booking is complete."""
        return self.current_participants >= self.min_participants


class BulkDiscount(models.Model):
    """Bulk discount model for group pricing."""
    
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_id = models.UUIDField(db_index=True)
    min_quantity = models.IntegerField()
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'bulk_discounts'
        indexes = [
            models.Index(fields=['event_id', 'is_active']),
        ]
    
    def __str__(self):
        return f"Discount for {self.min_quantity}+ tickets"
    
    def calculate_discount(self, quantity: int, base_price: Decimal) -> Decimal:
        """Calculate discount amount."""
        if quantity < self.min_quantity:
            return Decimal('0.00')
        
        if self.discount_type == 'percentage':
            return (base_price * self.discount_value / 100).quantize(Decimal('0.01'))
        else:
            return self.discount_value
    
    def apply_discount(self, quantity: int, total_price: Decimal) -> Decimal:
        """Apply discount to total price."""
        if quantity < self.min_quantity:
            return total_price
        
        discount = self.calculate_discount(quantity, total_price / quantity)
        return (total_price - (discount * quantity)).quantize(Decimal('0.01'))
