import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Waitlist(models.Model):
    """Waitlist domain model with business logic."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_id = models.UUIDField()
    user_id = models.UUIDField()
    
    # Waitlist details
    position = models.IntegerField()
    priority = models.IntegerField(default=0)  # Higher priority = promoted first
    
    # Status
    is_promoted = models.BooleanField(default=False)
    promoted_at = models.DateTimeField(null=True, blank=True)
    
    # Audit fields
    joined_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'waitlists'
        unique_together = [['event_id', 'user_id']]
        indexes = [
            models.Index(fields=['event_id', 'position']),
            models.Index(fields=['event_id', 'is_promoted']),
        ]
        ordering = ['position']
    
    def promote(self):
        """Promote from waitlist to registration."""
        if self.is_promoted:
            raise ValidationError('Already promoted from waitlist')
        self.is_promoted = True
        self.promoted_at = timezone.now()
        self.save()
    
    def update_position(self, new_position: int):
        """Update waitlist position."""
        if new_position < 1:
            raise ValidationError('Position must be at least 1')
        self.position = new_position
        self.save()
    
    def __str__(self):
        return f"Waitlist #{self.position} - Event {self.event_id}"
