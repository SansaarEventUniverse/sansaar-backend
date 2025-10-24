import uuid
import json
from django.test import TestCase, Client

from domain.venue import Venue


class VenueAPITest(TestCase):
    """Tests for Venue API endpoints."""
    
    def setUp(self):
        self.client = Client()
        self.owner_id = uuid.uuid4()
        
    def test_create_venue(self):
        """Test creating a venue via API."""
        data = {
            'name': 'Test Venue',
            'address': '123 Test St',
            'city': 'Test City',
            'state': 'Test State',
            'country': 'Test Country',
            'postal_code': '12345',
            'capacity': 100,
            'owner_id': str(self.owner_id),
        }
        response = self.client.post(
            '/api/venues/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['name'], 'Test Venue')
        
    def test_get_venue(self):
        """Test getting a venue via API."""
        venue = Venue.objects.create(
            name='Test Venue',
            address='123 Test St',
            city='Test City',
            state='Test State',
            country='Test Country',
            postal_code='12345',
            capacity=100,
            owner_id=self.owner_id,
        )
        response = self.client.get(f'/api/venues/{venue.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'Test Venue')
        
    def test_update_venue(self):
        """Test updating a venue via API."""
        venue = Venue.objects.create(
            name='Original Name',
            address='123 Test St',
            city='Test City',
            state='Test State',
            country='Test Country',
            postal_code='12345',
            capacity=100,
            owner_id=self.owner_id,
        )
        data = {'name': 'Updated Name'}
        response = self.client.patch(
            f'/api/venues/{venue.id}/update/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'Updated Name')
        
    def test_search_venues(self):
        """Test searching venues via API."""
        Venue.objects.create(
            name='NYC Venue',
            address='123 Test St',
            city='New York',
            state='NY',
            country='USA',
            postal_code='10001',
            capacity=100,
            owner_id=self.owner_id,
        )
        response = self.client.get('/api/venues/search/?city=New York')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['results'][0]['city'], 'New York')
