import uuid
from decimal import Decimal
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class TicketType(models.Model):
    """Ticket type model with business logic."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_id = models.UUIDField(db_index=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    quantity = models.IntegerField()
    quantity_sold = models.IntegerField(default=0)
    min_purchase = models.IntegerField(default=1)
    max_purchase = models.IntegerField(default=10)
    sale_start = models.DateTimeField()
    sale_end = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'ticket_types'
        indexes = [
            models.Index(fields=['event_id', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.event_id}"
    
    def clean(self):
        """Validate ticket type business rules."""
        if self.price < 0:
            raise ValidationError("Price cannot be negative")
        
        if self.quantity < 0:
            raise ValidationError("Quantity cannot be negative")
        
        if self.quantity_sold < 0:
            raise ValidationError("Quantity sold cannot be negative")
        
        if self.quantity_sold > self.quantity:
            raise ValidationError("Quantity sold cannot exceed total quantity")
        
        if self.min_purchase < 1:
            raise ValidationError("Minimum purchase must be at least 1")
        
        if self.max_purchase < self.min_purchase:
            raise ValidationError("Maximum purchase cannot be less than minimum purchase")
        
        if self.sale_end <= self.sale_start:
            raise ValidationError("Sale end must be after sale start")
    
    def available_quantity(self) -> int:
        """Get available ticket quantity."""
        return self.quantity - self.quantity_sold
    
    def is_available(self) -> bool:
        """Check if tickets are available for purchase."""
        now = timezone.now()
        return (
            self.is_active and
            self.available_quantity() > 0 and
            self.sale_start <= now <= self.sale_end
        )
    
    def can_purchase(self, quantity: int) -> bool:
        """Check if specified quantity can be purchased."""
        return (
            self.is_available() and
            self.min_purchase <= quantity <= self.max_purchase and
            quantity <= self.available_quantity()
        )
    
    def reserve_tickets(self, quantity: int) -> None:
        """Reserve tickets (increment sold count)."""
        if not self.can_purchase(quantity):
            raise ValidationError("Cannot reserve tickets")
        self.quantity_sold += quantity
        self.save()
    
    def release_tickets(self, quantity: int) -> None:
        """Release reserved tickets (decrement sold count)."""
        if quantity > self.quantity_sold:
            raise ValidationError("Cannot release more tickets than sold")
        self.quantity_sold -= quantity
        self.save()
