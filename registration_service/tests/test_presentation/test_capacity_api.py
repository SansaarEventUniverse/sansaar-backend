import uuid
import json
from django.test import TestCase, Client

from domain.capacity_rule import CapacityRule


class CapacityAPITest(TestCase):
    """Tests for Capacity API endpoints."""
    
    def setUp(self):
        self.client = Client()
        self.event_id = uuid.uuid4()
        
    def test_create_capacity_rule(self):
        """Test creating capacity rule via API."""
        data = {
            'max_capacity': 100,
            'warning_threshold': 80,
        }
        response = self.client.post(
            f'/api/registrations/events/{self.event_id}/capacity/rule/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['max_capacity'], 100)
        
    def test_get_capacity(self):
        """Test getting capacity info via API."""
        CapacityRule.objects.create(
            event_id=self.event_id,
            max_capacity=100,
            warning_threshold=80,
        )
        response = self.client.get(
            f'/api/registrations/events/{self.event_id}/capacity/info/'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['max_capacity'], 100)
        self.assertIn('available', data)
