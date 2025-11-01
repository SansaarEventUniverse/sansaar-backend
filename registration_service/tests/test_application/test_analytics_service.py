import uuid
from django.test import TestCase

from domain.registration import Registration
from domain.waitlist import Waitlist
from domain.group_registration import GroupRegistration
from domain.capacity_rule import CapacityRule
from application.analytics_service import (
    GenerateAnalyticsService,
    RegistrationReportService,
)


class GenerateAnalyticsServiceTest(TestCase):
    """Tests for GenerateAnalyticsService."""
    
    def test_generate_analytics(self):
        """Test generating analytics."""
        event_id = uuid.uuid4()
        
        # Create test data
        Registration.objects.create(
            event_id=event_id,
            user_id=uuid.uuid4(),
            status='confirmed',
            attendee_name='John Doe',
            attendee_email='john@example.com',
        )
        
        Waitlist.objects.create(
            event_id=event_id,
            user_id=uuid.uuid4(),
            position=1,
        )
        
        service = GenerateAnalyticsService()
        analytics = service.execute(event_id)
        
        self.assertEqual(analytics.total_registrations, 1)
        self.assertEqual(analytics.confirmed_registrations, 1)
        self.assertEqual(analytics.total_waitlist, 1)


class RegistrationReportServiceTest(TestCase):
    """Tests for RegistrationReportService."""
    
    def test_generate_report(self):
        """Test generating registration report."""
        event_id = uuid.uuid4()
        
        Registration.objects.create(
            event_id=event_id,
            user_id=uuid.uuid4(),
            status='confirmed',
            attendee_name='John Doe',
            attendee_email='john@example.com',
        )
        
        service = RegistrationReportService()
        report = service.execute(event_id)
        
        self.assertEqual(report['registrations']['total'], 1)
        self.assertEqual(report['registrations']['confirmed'], 1)
        self.assertIn('waitlist', report)
        self.assertIn('groups', report)
