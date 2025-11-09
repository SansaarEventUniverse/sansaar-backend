import uuid
from django.db import models
from django.core.exceptions import ValidationError
import pytz


class CalendarEvent(models.Model):
    """Calendar event model for external calendar integration."""
    
    SYNC_STATUS = [
        ('pending', 'Pending'),
        ('synced', 'Synced'),
        ('failed', 'Failed'),
    ]
    
    CALENDAR_PROVIDER = [
        ('google', 'Google Calendar'),
        ('outlook', 'Outlook Calendar'),
        ('apple', 'Apple Calendar'),
        ('ical', 'iCal'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_id = models.UUIDField(db_index=True)
    user_id = models.UUIDField(db_index=True)
    
    # Calendar provider info
    provider = models.CharField(max_length=20, choices=CALENDAR_PROVIDER)
    external_calendar_id = models.CharField(max_length=255, blank=True)
    external_event_id = models.CharField(max_length=255, blank=True)
    
    # Sync info
    sync_status = models.CharField(max_length=20, choices=SYNC_STATUS, default='pending')
    sync_token = models.CharField(max_length=500, blank=True)
    last_synced_at = models.DateTimeField(null=True, blank=True)
    sync_error = models.TextField(blank=True)
    
    # Event details (cached for quick access)
    event_title = models.CharField(max_length=255)
    event_start = models.DateTimeField()
    event_end = models.DateTimeField()
    event_timezone = models.CharField(max_length=100)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'calendar_events'
        indexes = [
            models.Index(fields=['event_id', 'user_id']),
            models.Index(fields=['provider', 'sync_status']),
            models.Index(fields=['external_event_id']),
        ]
        unique_together = [['event_id', 'user_id', 'provider']]
    
    def validate_timezone(self) -> None:
        """Validate event timezone."""
        try:
            pytz.timezone(self.event_timezone)
        except pytz.exceptions.UnknownTimeZoneError:
            raise ValidationError(f"Invalid timezone: {self.event_timezone}")
    
    def mark_synced(self, external_event_id: str) -> None:
        """Mark calendar event as synced."""
        from django.utils import timezone
        self.sync_status = 'synced'
        self.external_event_id = external_event_id
        self.last_synced_at = timezone.now()
        self.sync_error = ''
        self.save()
    
    def mark_failed(self, error: str) -> None:
        """Mark calendar event sync as failed."""
        self.sync_status = 'failed'
        self.sync_error = error
        self.save()
    
    def needs_sync(self) -> bool:
        """Check if event needs syncing."""
        return self.sync_status in ['pending', 'failed']
    
    def convert_to_timezone(self, target_tz: str) -> tuple:
        """Convert event times to target timezone."""
        try:
            source_tz = pytz.timezone(self.event_timezone)
            target_tz_obj = pytz.timezone(target_tz)
            
            start_local = self.event_start.replace(tzinfo=pytz.UTC).astimezone(source_tz)
            end_local = self.event_end.replace(tzinfo=pytz.UTC).astimezone(source_tz)
            
            start_target = start_local.astimezone(target_tz_obj)
            end_target = end_local.astimezone(target_tz_obj)
            
            return (start_target, end_target)
        except pytz.exceptions.UnknownTimeZoneError:
            raise ValidationError(f"Invalid timezone: {target_tz}")
    
    def __str__(self):
        return f"{self.event_title} - {self.provider} ({self.sync_status})"
