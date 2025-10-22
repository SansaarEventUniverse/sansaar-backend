import uuid
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
import pytz

from application.datetime_service import (
    DateTimeValidationService,
    ICalExportService,
    TimezoneConversionService,
)
from domain.event import Event


class DateTimeValidationServiceTest(TestCase):
    """Tests for DateTimeValidationService."""
    
    def setUp(self):
        self.service = DateTimeValidationService()
        self.now = timezone.now()
        
    def test_valid_datetime(self):
        """Test valid date/time validation."""
        result = self.service.execute(
            self.now + timedelta(days=1),
            self.now + timedelta(days=2),
            'UTC'
        )
        self.assertTrue(result)
        
    def test_invalid_timezone(self):
        """Test invalid timezone."""
        with self.assertRaises(ValidationError):
            self.service.execute(
                self.now + timedelta(days=1),
                self.now + timedelta(days=2),
                'Invalid/Timezone'
            )
            
    def test_start_after_end(self):
        """Test start after end validation."""
        with self.assertRaises(ValidationError):
            self.service.execute(
                self.now + timedelta(days=2),
                self.now + timedelta(days=1),
                'UTC'
            )


class ICalExportServiceTest(TestCase):
    """Tests for ICalExportService."""
    
    def setUp(self):
        self.service = ICalExportService()
        self.organizer_id = uuid.uuid4()
        self.venue_id = uuid.uuid4()
        self.now = timezone.now()
        
    def test_export_ical(self):
        """Test iCal export."""
        event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            organizer_id=self.organizer_id,
            start_datetime=self.now + timedelta(days=1),
            end_datetime=self.now + timedelta(days=2),
            venue_id=self.venue_id,
        )
        ical = self.service.execute(event.id)
        self.assertIn('BEGIN:VCALENDAR', ical)
        self.assertIn('Test Event', ical)
        self.assertIn(str(event.id), ical)
        
    def test_export_nonexistent_event(self):
        """Test exporting non-existent event."""
        with self.assertRaises(ValidationError):
            self.service.execute(uuid.uuid4())


class TimezoneConversionServiceTest(TestCase):
    """Tests for TimezoneConversionService."""
    
    def setUp(self):
        self.service = TimezoneConversionService()
        
    def test_convert_timezone(self):
        """Test timezone conversion."""
        utc_time = timezone.now()
        ny_time = self.service.convert_to_timezone(utc_time, 'America/New_York')
        self.assertIsNotNone(ny_time.tzinfo)
        
    def test_invalid_timezone(self):
        """Test invalid timezone conversion."""
        with self.assertRaises(ValidationError):
            self.service.convert_to_timezone(timezone.now(), 'Invalid/Timezone')
