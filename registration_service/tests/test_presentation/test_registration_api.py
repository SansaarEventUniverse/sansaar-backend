import uuid
import json
from django.test import TestCase, Client

from domain.registration import Registration


class RegistrationAPITest(TestCase):
    """Tests for Registration API endpoints."""
    
    def setUp(self):
        self.client = Client()
        self.event_id = uuid.uuid4()
        self.user_id = uuid.uuid4()
        
    def test_register_for_event(self):
        """Test registering for an event via API."""
        data = {
            'user_id': str(self.user_id),
            'attendee_name': 'John Doe',
            'attendee_email': 'john@example.com',
        }
        response = self.client.post(
            f'/api/registrations/events/{self.event_id}/register/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['attendee_name'], 'John Doe')
        
    def test_cancel_registration(self):
        """Test cancelling a registration via API."""
        Registration.objects.create(
            event_id=self.event_id,
            user_id=self.user_id,
            attendee_name='John Doe',
            attendee_email='john@example.com',
        )
        data = {'user_id': str(self.user_id)}
        response = self.client.delete(
            f'/api/registrations/events/{self.event_id}/cancel/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'cancelled')
        
    def test_get_event_registrations(self):
        """Test getting event registrations via API."""
        Registration.objects.create(
            event_id=self.event_id,
            user_id=self.user_id,
            attendee_name='John Doe',
            attendee_email='john@example.com',
        )
        response = self.client.get(
            f'/api/registrations/events/{self.event_id}/'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['count'], 1)
        
    def test_check_capacity(self):
        """Test checking capacity via API."""
        Registration.objects.create(
            event_id=self.event_id,
            user_id=self.user_id,
            attendee_name='John Doe',
            attendee_email='john@example.com',
        )
        response = self.client.get(
            f'/api/registrations/events/{self.event_id}/capacity/?max_capacity=10'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['confirmed_count'], 1)
        self.assertTrue(data['has_capacity'])
