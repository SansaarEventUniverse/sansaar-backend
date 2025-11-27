import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class OfflineTicket(models.Model):
    """Offline ticket model for validation without internet."""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('used', 'Used'),
        ('expired', 'Expired'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket_id = models.UUIDField(db_index=True)
    qr_code = models.CharField(max_length=255, unique=True)
    event_id = models.UUIDField(db_index=True)
    attendee_name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    valid_until = models.DateTimeField()
    last_synced = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'offline_tickets'
        indexes = [
            models.Index(fields=['ticket_id', 'status']),
            models.Index(fields=['event_id']),
        ]
    
    def __str__(self):
        return f"Offline Ticket {self.ticket_id}"
    
    def is_valid(self) -> bool:
        """Check if ticket is valid for offline use."""
        return self.status == 'active' and self.valid_until > timezone.now()
    
    def validate_offline(self) -> bool:
        """Validate ticket offline."""
        if not self.is_valid():
            raise ValidationError("Ticket is not valid")
        if self.status == 'used':
            raise ValidationError("Ticket already used")
        return True
    
    def mark_used(self) -> None:
        """Mark ticket as used."""
        if self.status == 'used':
            raise ValidationError("Ticket already used")
        self.status = 'used'
        self.save()


class ValidationCache(models.Model):
    """Cache for offline validation data."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_id = models.UUIDField(db_index=True)
    cache_data = models.JSONField(default=dict)
    ticket_count = models.IntegerField(default=0)
    last_synced = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'validation_cache'
        indexes = [
            models.Index(fields=['event_id', 'expires_at']),
        ]
    
    def __str__(self):
        return f"Cache for Event {self.event_id}"
    
    def is_expired(self) -> bool:
        """Check if cache is expired."""
        return self.expires_at < timezone.now()
    
    def update_cache(self, data: dict) -> None:
        """Update cache data."""
        self.cache_data = data
        self.ticket_count = len(data.get('tickets', []))
        self.save()
