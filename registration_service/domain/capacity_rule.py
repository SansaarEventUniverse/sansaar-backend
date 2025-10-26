import uuid
from django.db import models
from django.core.exceptions import ValidationError


class CapacityRule(models.Model):
    """Capacity rule model for advanced capacity management."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_id = models.UUIDField(unique=True)
    
    # Capacity limits
    max_capacity = models.IntegerField()
    warning_threshold = models.IntegerField()  # Percentage (e.g., 80 for 80%)
    
    # Reservation settings
    allow_reservations = models.BooleanField(default=True)
    reservation_timeout_minutes = models.IntegerField(default=15)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'capacity_rules'
        indexes = [
            models.Index(fields=['event_id']),
        ]
    
    def clean(self):
        """Validate capacity rule."""
        errors = {}
        
        if self.max_capacity < 1:
            errors['max_capacity'] = 'Max capacity must be at least 1'
        
        if self.warning_threshold < 0 or self.warning_threshold > 100:
            errors['warning_threshold'] = 'Warning threshold must be between 0 and 100'
        
        if self.reservation_timeout_minutes < 1:
            errors['reservation_timeout_minutes'] = 'Timeout must be at least 1 minute'
        
        if errors:
            raise ValidationError(errors)
    
    def is_at_capacity(self, current_count: int) -> bool:
        """Check if at capacity."""
        return current_count >= self.max_capacity
    
    def is_near_capacity(self, current_count: int) -> bool:
        """Check if near capacity threshold."""
        threshold = (self.max_capacity * self.warning_threshold) / 100
        return current_count >= threshold
    
    def available_spots(self, current_count: int) -> int:
        """Get available spots."""
        return max(0, self.max_capacity - current_count)
    
    def __str__(self):
        return f"Capacity Rule for Event {self.event_id}"
