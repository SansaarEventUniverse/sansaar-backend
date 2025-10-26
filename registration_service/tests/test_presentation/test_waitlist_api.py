import uuid
import json
from django.test import TestCase, Client

from domain.waitlist import Waitlist


class WaitlistAPITest(TestCase):
    """Tests for Waitlist API endpoints."""
    
    def setUp(self):
        self.client = Client()
        self.event_id = uuid.uuid4()
        self.user_id = uuid.uuid4()
        
    def test_join_waitlist(self):
        """Test joining waitlist via API."""
        data = {'user_id': str(self.user_id)}
        response = self.client.post(
            f'/api/registrations/events/{self.event_id}/waitlist/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['position'], 1)
        
    def test_get_waitlist_position(self):
        """Test getting waitlist position via API."""
        Waitlist.objects.create(
            event_id=self.event_id,
            user_id=self.user_id,
            position=1,
        )
        response = self.client.get(
            f'/api/registrations/events/{self.event_id}/waitlist/position/?user_id={self.user_id}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['position'], 1)
        
    def test_get_event_waitlist(self):
        """Test getting event waitlist via API."""
        Waitlist.objects.create(
            event_id=self.event_id,
            user_id=self.user_id,
            position=1,
        )
        response = self.client.get(
            f'/api/registrations/events/{self.event_id}/waitlist/list/'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['count'], 1)
