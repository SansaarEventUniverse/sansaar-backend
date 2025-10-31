import uuid
from django.test import TestCase, Client

from domain.registration import Registration
from domain.waitlist import Waitlist


class AnalyticsAPITest(TestCase):
    """Tests for Analytics API endpoints."""
    
    def setUp(self):
        self.client = Client()
        self.event_id = uuid.uuid4()
        
    def test_get_analytics(self):
        """Test getting analytics via API."""
        Registration.objects.create(
            event_id=self.event_id,
            user_id=uuid.uuid4(),
            status='confirmed',
            attendee_name='John Doe',
            attendee_email='john@example.com',
        )
        
        response = self.client.get(
            f'/api/registrations/events/{self.event_id}/analytics/'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['total_registrations'], 1)
        
    def test_get_dashboard(self):
        """Test getting dashboard data via API."""
        Registration.objects.create(
            event_id=self.event_id,
            user_id=uuid.uuid4(),
            status='confirmed',
            attendee_name='John Doe',
            attendee_email='john@example.com',
        )
        
        response = self.client.get(
            f'/api/registrations/events/{self.event_id}/analytics/dashboard/'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('registrations', response.json())
        self.assertIn('waitlist', response.json())
        
    def test_export_analytics(self):
        """Test exporting analytics via API."""
        response = self.client.get(
            f'/api/registrations/events/{self.event_id}/analytics/export/'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['export_format'], 'json')
