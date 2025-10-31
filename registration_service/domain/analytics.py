import uuid
from django.db import models
from decimal import Decimal


class RegistrationAnalytics(models.Model):
    """Registration analytics model for event metrics."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_id = models.UUIDField(unique=True)
    
    # Registration metrics
    total_registrations = models.IntegerField(default=0)
    confirmed_registrations = models.IntegerField(default=0)
    cancelled_registrations = models.IntegerField(default=0)
    
    # Waitlist metrics
    total_waitlist = models.IntegerField(default=0)
    promoted_from_waitlist = models.IntegerField(default=0)
    
    # Group metrics
    total_groups = models.IntegerField(default=0)
    total_group_members = models.IntegerField(default=0)
    
    # Capacity metrics
    capacity_utilization = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # Timestamps
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'registration_analytics'
        indexes = [
            models.Index(fields=['event_id']),
        ]
    
    def calculate_utilization(self, max_capacity: int) -> Decimal:
        """Calculate capacity utilization percentage."""
        if max_capacity == 0:
            return Decimal('0.00')
        return Decimal(str((self.confirmed_registrations / max_capacity) * 100))
    
    def get_conversion_rate(self) -> Decimal:
        """Calculate waitlist to registration conversion rate."""
        if self.promoted_from_waitlist == 0:
            return Decimal('0.00')
        return Decimal(str((self.promoted_from_waitlist / self.total_waitlist) * 100))
    
    def __str__(self):
        return f"Analytics for Event {self.event_id}"
