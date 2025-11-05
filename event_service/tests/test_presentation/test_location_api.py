import uuid
from django.test import TestCase, Client

from domain.location import EventLocation


class LocationAPITest(TestCase):
    """Tests for Location API endpoints."""
    
    def setUp(self):
        self.client = Client()
        
        EventLocation.objects.create(
            event_id=uuid.uuid4(),
            address='123 Main St',
            city='San Francisco',
            country='USA',
            latitude=37.7749,
            longitude=-122.4194,
        )
        EventLocation.objects.create(
            event_id=uuid.uuid4(),
            address='456 Oak St',
            city='Oakland',
            country='USA',
            latitude=37.8044,
            longitude=-122.2712,
        )
        
    def test_search_nearby(self):
        """Test searching nearby events via API."""
        response = self.client.get(
            '/api/events/nearby/?latitude=37.7749&longitude=-122.4194&radius_km=20'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('results', data)
        self.assertEqual(data['count'], 2)
        
    def test_search_by_city(self):
        """Test searching by city via API."""
        response = self.client.get('/api/events/search/location/?city=San Francisco')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['results'][0]['city'], 'San Francisco')
        
    def test_get_map_events(self):
        """Test getting events for map via API."""
        response = self.client.get(
            '/api/events/map/?min_lat=37.0&max_lat=38.0&min_lon=-123.0&max_lon=-122.0'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('events', data)
        self.assertEqual(data['count'], 2)
