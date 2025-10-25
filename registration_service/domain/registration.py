import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Registration(models.Model):
    """Registration domain model with business logic."""
    
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('waitlisted', 'Waitlisted'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_id = models.UUIDField()
    user_id = models.UUIDField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    
    # Registration details
    attendee_name = models.CharField(max_length=255)
    attendee_email = models.EmailField()
    attendee_phone = models.CharField(max_length=20, blank=True)
    
    # Audit fields
    registered_at = models.DateTimeField(auto_now_add=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'registrations'
        unique_together = [['event_id', 'user_id']]
        indexes = [
            models.Index(fields=['event_id']),
            models.Index(fields=['user_id']),
            models.Index(fields=['status']),
        ]
    
    def clean(self):
        """Validate registration business rules."""
        errors = {}
        
        if self.status == 'cancelled' and not self.cancelled_at:
            errors['cancelled_at'] = 'Cancelled registrations must have cancelled_at timestamp'
        
        if errors:
            raise ValidationError(errors)
    
    def cancel(self):
        """Cancel the registration."""
        if self.status == 'cancelled':
            raise ValidationError('Registration is already cancelled')
        self.status = 'cancelled'
        self.cancelled_at = timezone.now()
        self.save()
    
    def confirm(self):
        """Confirm a waitlisted registration."""
        if self.status != 'waitlisted':
            raise ValidationError('Only waitlisted registrations can be confirmed')
        self.status = 'confirmed'
        self.save()
    
    def is_active(self):
        """Check if registration is active."""
        return self.status == 'confirmed'
    
    def __str__(self):
        return f"{self.attendee_name} - {self.event_id}"
