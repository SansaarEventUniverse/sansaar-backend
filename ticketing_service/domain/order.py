import uuid
from decimal import Decimal
from django.db import models
from django.core.exceptions import ValidationError


class Order(models.Model):
    """Order model for ticket purchases."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(db_index=True)
    event_id = models.UUIDField(db_index=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_id = models.UUIDField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'orders'
        indexes = [
            models.Index(fields=['user_id', 'status']),
            models.Index(fields=['event_id']),
        ]
    
    def __str__(self):
        return f"Order {self.id} - {self.total_amount} {self.currency}"
    
    def clean(self):
        """Validate order business rules."""
        if self.total_amount < 0:
            raise ValidationError("Total amount cannot be negative")
    
    def calculate_total(self):
        """Calculate total from order items."""
        total = sum(item.subtotal for item in self.items.all())
        self.total_amount = total
        self.save()
    
    def confirm(self, payment_id: uuid.UUID):
        """Confirm the order."""
        if self.status != 'pending':
            raise ValidationError("Only pending orders can be confirmed")
        self.status = 'confirmed'
        self.payment_id = payment_id
        self.save()
    
    def cancel(self):
        """Cancel the order."""
        if self.status == 'confirmed':
            raise ValidationError("Cannot cancel confirmed order")
        self.status = 'cancelled'
        self.save()
    
    def can_purchase(self) -> bool:
        """Check if order can be purchased."""
        return self.status == 'pending' and self.items.exists()


class OrderItem(models.Model):
    """Order item for individual tickets."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    ticket_type_id = models.UUIDField()
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'order_items'
    
    def __str__(self):
        return f"OrderItem {self.id} - {self.quantity}x @ {self.unit_price}"
    
    def clean(self):
        """Validate order item business rules."""
        if self.quantity <= 0:
            raise ValidationError("Quantity must be positive")
        if self.unit_price < 0:
            raise ValidationError("Unit price cannot be negative")
    
    def save(self, *args, **kwargs):
        """Calculate subtotal before saving."""
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)
