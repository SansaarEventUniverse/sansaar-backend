import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Event(models.Model):
    """Event domain model with business logic."""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
        ('unlisted', 'Unlisted'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=10000)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='public')
    
    # Organizer info
    organizer_id = models.UUIDField()
    organization_id = models.UUIDField(null=True, blank=True)
    
    # Date and time
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    timezone = models.CharField(max_length=50, default='UTC')
    is_all_day = models.BooleanField(default=False)
    
    # Venue
    venue_id = models.UUIDField(null=True, blank=True)
    is_online = models.BooleanField(default=False)
    online_url = models.URLField(max_length=500, null=True, blank=True)
    
    # Capacity
    max_attendees = models.IntegerField(null=True, blank=True)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'events'
        indexes = [
            models.Index(fields=['organizer_id']),
            models.Index(fields=['organization_id']),
            models.Index(fields=['status']),
            models.Index(fields=['start_datetime']),
            models.Index(fields=['deleted_at']),
        ]
    
    def clean(self):
        """Validate event business rules."""
        errors = {}
        
        if self.end_datetime and self.start_datetime >= self.end_datetime:
            errors['end_datetime'] = 'End datetime must be after start datetime'
        
        if self.is_online and not self.online_url:
            errors['online_url'] = 'Online URL is required for online events'
        
        if not self.is_online and not self.venue_id:
            errors['venue_id'] = 'Venue is required for in-person events'
        
        if self.max_attendees and self.max_attendees < 1:
            errors['max_attendees'] = 'Max attendees must be at least 1'
        
        if errors:
            raise ValidationError(errors)
    
    def publish(self):
        """Publish the event."""
        if self.status != 'draft':
            raise ValidationError('Only draft events can be published')
        self.status = 'published'
        self.save()
    
    def cancel(self):
        """Cancel the event."""
        if self.status in ['completed', 'cancelled']:
            raise ValidationError(f'Cannot cancel {self.status} event')
        self.status = 'cancelled'
        self.save()
    
    def complete(self):
        """Mark event as completed."""
        if self.status != 'published':
            raise ValidationError('Only published events can be completed')
        if timezone.now() < self.end_datetime:
            raise ValidationError('Cannot complete event before end datetime')
        self.status = 'completed'
        self.save()
    
    def is_past(self):
        """Check if event has ended."""
        return timezone.now() > self.end_datetime
    
    def is_upcoming(self):
        """Check if event is upcoming."""
        return timezone.now() < self.start_datetime
    
    def is_ongoing(self):
        """Check if event is currently happening."""
        now = timezone.now()
        return self.start_datetime <= now <= self.end_datetime
    
    def soft_delete(self):
        """Soft delete the event."""
        self.deleted_at = timezone.now()
        self.save()
    
    def __str__(self):
        return f"{self.title} ({self.status})"


class EventDraft(models.Model):
    """Auto-save draft for event creation."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_id = models.UUIDField(null=True, blank=True)
    organizer_id = models.UUIDField()
    
    # Draft data stored as JSON
    draft_data = models.JSONField()
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'event_drafts'
        indexes = [
            models.Index(fields=['organizer_id']),
            models.Index(fields=['event_id']),
            models.Index(fields=['updated_at']),
        ]
    
    def __str__(self):
        return f"Draft for {self.event_id or 'new event'} by {self.organizer_id}"
