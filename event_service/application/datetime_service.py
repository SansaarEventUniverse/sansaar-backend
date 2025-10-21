import uuid
from datetime import datetime
import pytz
from django.core.exceptions import ValidationError

from domain.event import Event


class DateTimeValidationService:
    """Service for validating event date/time."""
    
    def execute(self, start_datetime: datetime, end_datetime: datetime, 
                event_timezone: str) -> bool:
        """Validate event date/time."""
        # Validate timezone
        try:
            tz = pytz.timezone(event_timezone)
        except pytz.exceptions.UnknownTimeZoneError:
            raise ValidationError(f'Invalid timezone: {event_timezone}')
        
        # Validate start before end
        if start_datetime >= end_datetime:
            raise ValidationError('Start datetime must be before end datetime')
        
        return True


class ICalExportService:
    """Service for exporting events to iCal format."""
    
    def execute(self, event_id: uuid.UUID) -> str:
        """Generate iCal file content for an event."""
        try:
            event = Event.objects.get(id=event_id, deleted_at__isnull=True)
        except Event.DoesNotExist:
            raise ValidationError('Event not found')
        
        # Format datetimes for iCal
        start = event.start_datetime.strftime('%Y%m%dT%H%M%SZ')
        end = event.end_datetime.strftime('%Y%m%dT%H%M%SZ')
        created = event.created_at.strftime('%Y%m%dT%H%M%SZ')
        updated = event.updated_at.strftime('%Y%m%dT%H%M%SZ')
        
        ical = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Sansaar Event Universe//EN
BEGIN:VEVENT
UID:{event.id}@sansaar.com
DTSTAMP:{created}
DTSTART:{start}
DTEND:{end}
SUMMARY:{event.title}
DESCRIPTION:{event.description}
STATUS:{event.status.upper()}
LAST-MODIFIED:{updated}
END:VEVENT
END:VCALENDAR"""
        
        return ical


class TimezoneConversionService:
    """Service for timezone conversions."""
    
    def convert_to_timezone(self, dt: datetime, target_timezone: str) -> datetime:
        """Convert datetime to target timezone."""
        try:
            tz = pytz.timezone(target_timezone)
        except pytz.exceptions.UnknownTimeZoneError:
            raise ValidationError(f'Invalid timezone: {target_timezone}')
        
        if dt.tzinfo is None:
            dt = pytz.utc.localize(dt)
        
        return dt.astimezone(tz)
