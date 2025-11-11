import uuid
from datetime import datetime
from django.test import TestCase
from django.core.exceptions import ValidationError
import pytz

from domain.calendar import CalendarEvent
from domain.event import Event
from application.calendar_service import (
    CalendarSyncService,
    ICalExportService,
    GoogleCalendarService,
    CalendarEventManagementService,
)


class CalendarSyncServiceTest(TestCase):
    """Tests for CalendarSyncService."""
    
    def test_create_sync(self):
        """Test creating calendar sync."""
        event = Event.objects.create(
            title='Test Event',
            description='Test',
            start_datetime=datetime(2026, 2, 1, 10, 0, tzinfo=pytz.UTC),
            end_datetime=datetime(2026, 2, 1, 12, 0, tzinfo=pytz.UTC),
            timezone='UTC',
            organizer_id=uuid.uuid4(),
        )
        
        service = CalendarSyncService()
        cal_event = service.create_sync(event.id, uuid.uuid4(), 'google')
        
        self.assertEqual(cal_event.event_id, event.id)
        self.assertEqual(cal_event.provider, 'google')
        self.assertEqual(cal_event.sync_status, 'pending')
        
    def test_get_pending_syncs(self):
        """Test getting pending syncs."""
        event = Event.objects.create(
            title='Test Event',
            description='Test',
            start_datetime=datetime(2026, 2, 1, 10, 0, tzinfo=pytz.UTC),
            end_datetime=datetime(2026, 2, 1, 12, 0, tzinfo=pytz.UTC),
            timezone='UTC',
            organizer_id=uuid.uuid4(),
        )
        
        service = CalendarSyncService()
        service.create_sync(event.id, uuid.uuid4(), 'google')
        
        pending = service.get_pending_syncs()
        self.assertEqual(len(pending), 1)
        
    def test_mark_synced(self):
        """Test marking sync as complete."""
        event = Event.objects.create(
            title='Test Event',
            description='Test',
            start_datetime=datetime(2026, 2, 1, 10, 0, tzinfo=pytz.UTC),
            end_datetime=datetime(2026, 2, 1, 12, 0, tzinfo=pytz.UTC),
            timezone='UTC',
            organizer_id=uuid.uuid4(),
        )
        
        service = CalendarSyncService()
        cal_event = service.create_sync(event.id, uuid.uuid4(), 'google')
        service.mark_synced(cal_event.id, 'external-123')
        
        cal_event.refresh_from_db()
        self.assertEqual(cal_event.sync_status, 'synced')


class ICalExportServiceTest(TestCase):
    """Tests for ICalExportService."""
    
    def test_export_event(self):
        """Test exporting event to iCal."""
        event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            start_datetime=datetime(2026, 2, 1, 10, 0, tzinfo=pytz.UTC),
            end_datetime=datetime(2026, 2, 1, 12, 0, tzinfo=pytz.UTC),
            timezone='UTC',
            organizer_id=uuid.uuid4(),
        )
        
        service = ICalExportService()
        ical = service.export_event(event.id)
        
        self.assertIn('BEGIN:VCALENDAR', ical)
        self.assertIn('BEGIN:VEVENT', ical)
        self.assertIn('Test Event', ical)
        self.assertIn('END:VCALENDAR', ical)


class GoogleCalendarServiceTest(TestCase):
    """Tests for GoogleCalendarService."""
    
    def test_sync_event(self):
        """Test syncing event to Google Calendar."""
        cal_event = CalendarEvent.objects.create(
            event_id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            provider='google',
            event_title='Test Event',
            event_start=datetime(2026, 2, 1, 10, 0, tzinfo=pytz.UTC),
            event_end=datetime(2026, 2, 1, 12, 0, tzinfo=pytz.UTC),
            event_timezone='UTC',
        )
        
        service = GoogleCalendarService()
        external_id = service.sync_event(cal_event)
        
        self.assertIsNotNone(external_id)
        self.assertIn('google-', external_id)


class CalendarEventManagementServiceTest(TestCase):
    """Tests for CalendarEventManagementService."""
    
    def test_sync_to_calendar(self):
        """Test syncing event to calendar."""
        event = Event.objects.create(
            title='Test Event',
            description='Test',
            start_datetime=datetime(2026, 2, 1, 10, 0, tzinfo=pytz.UTC),
            end_datetime=datetime(2026, 2, 1, 12, 0, tzinfo=pytz.UTC),
            timezone='UTC',
            organizer_id=uuid.uuid4(),
        )
        
        service = CalendarEventManagementService()
        cal_event = service.sync_to_calendar(event.id, uuid.uuid4(), 'google')
        
        self.assertEqual(cal_event.sync_status, 'synced')
        self.assertIsNotNone(cal_event.external_event_id)
        
    def test_export_to_ical(self):
        """Test exporting to iCal."""
        event = Event.objects.create(
            title='Test Event',
            description='Test',
            start_datetime=datetime(2026, 2, 1, 10, 0, tzinfo=pytz.UTC),
            end_datetime=datetime(2026, 2, 1, 12, 0, tzinfo=pytz.UTC),
            timezone='UTC',
            organizer_id=uuid.uuid4(),
        )
        
        service = CalendarEventManagementService()
        ical = service.export_to_ical(event.id)
        
        self.assertIn('BEGIN:VCALENDAR', ical)
