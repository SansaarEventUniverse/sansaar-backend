import uuid
from typing import Dict, Optional
from datetime import datetime
from django.core.exceptions import ValidationError

from domain.calendar import CalendarEvent
from domain.event import Event


class CalendarSyncService:
    """Service for syncing events to external calendars."""
    
    def create_sync(
        self, event_id: uuid.UUID, user_id: uuid.UUID, provider: str, 
        external_calendar_id: str = ''
    ) -> CalendarEvent:
        """Create calendar sync entry."""
        try:
            event = Event.objects.get(id=event_id, deleted_at__isnull=True)
        except Event.DoesNotExist:
            raise ValidationError("Event not found")
        
        cal_event = CalendarEvent.objects.create(
            event_id=event_id,
            user_id=user_id,
            provider=provider,
            external_calendar_id=external_calendar_id,
            event_title=event.title,
            event_start=event.start_datetime,
            event_end=event.end_datetime,
            event_timezone=event.timezone,
        )
        
        cal_event.validate_timezone()
        return cal_event
    
    def get_pending_syncs(self, provider: Optional[str] = None) -> list:
        """Get pending calendar syncs."""
        query = CalendarEvent.objects.filter(sync_status='pending')
        if provider:
            query = query.filter(provider=provider)
        return list(query)
    
    def mark_synced(self, calendar_event_id: uuid.UUID, external_event_id: str) -> None:
        """Mark calendar event as synced."""
        try:
            cal_event = CalendarEvent.objects.get(id=calendar_event_id)
            cal_event.mark_synced(external_event_id)
        except CalendarEvent.DoesNotExist:
            raise ValidationError("Calendar event not found")


class ICalExportService:
    """Service for exporting events to iCal format."""
    
    def export_event(self, event_id: uuid.UUID) -> str:
        """Generate iCal file content for an event."""
        try:
            event = Event.objects.get(id=event_id, deleted_at__isnull=True)
        except Event.DoesNotExist:
            raise ValidationError("Event not found")
        
        start = event.start_datetime.strftime('%Y%m%dT%H%M%SZ')
        end = event.end_datetime.strftime('%Y%m%dT%H%M%SZ')
        created = event.created_at.strftime('%Y%m%dT%H%M%SZ')
        
        ical = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Sansaar Event Universe//EN
CALSCALE:GREGORIAN
BEGIN:VEVENT
UID:{event.id}@sansaar.com
DTSTAMP:{created}
DTSTART:{start}
DTEND:{end}
SUMMARY:{event.title}
DESCRIPTION:{event.description[:500] if event.description else ''}
STATUS:CONFIRMED
END:VEVENT
END:VCALENDAR"""
        
        return ical


class GoogleCalendarService:
    """Service for Google Calendar integration."""
    
    def sync_event(self, calendar_event: CalendarEvent) -> str:
        """Sync event to Google Calendar."""
        # Mock implementation - would use Google Calendar API
        external_event_id = f"google-{uuid.uuid4()}"
        return external_event_id
    
    def update_event(self, external_event_id: str, event_data: Dict) -> bool:
        """Update event in Google Calendar."""
        # Mock implementation
        return True
    
    def delete_event(self, external_event_id: str) -> bool:
        """Delete event from Google Calendar."""
        # Mock implementation
        return True


class CalendarEventManagementService:
    """Service for managing calendar events."""
    
    def __init__(self):
        self.sync_service = CalendarSyncService()
        self.ical_service = ICalExportService()
        self.google_service = GoogleCalendarService()
    
    def sync_to_calendar(
        self, event_id: uuid.UUID, user_id: uuid.UUID, provider: str
    ) -> CalendarEvent:
        """Sync event to external calendar."""
        cal_event = self.sync_service.create_sync(event_id, user_id, provider)
        
        if provider == 'google':
            try:
                external_id = self.google_service.sync_event(cal_event)
                self.sync_service.mark_synced(cal_event.id, external_id)
                cal_event.refresh_from_db()
            except Exception as e:
                cal_event.mark_failed(str(e))
        
        return cal_event
    
    def export_to_ical(self, event_id: uuid.UUID) -> str:
        """Export event to iCal format."""
        return self.ical_service.export_event(event_id)
