import uuid
from django.test import TestCase
from django.core.exceptions import ValidationError

from application.venue_service import (
    CreateVenueService,
    UpdateVenueService,
    SearchVenueService,
    GetVenueService,
)
from domain.venue import Venue


class CreateVenueServiceTest(TestCase):
    """Tests for CreateVenueService."""
    
    def setUp(self):
        self.service = CreateVenueService()
        self.owner_id = uuid.uuid4()
        
    def test_create_venue(self):
        """Test creating a venue."""
        data = {
            'name': 'Test Venue',
            'address': '123 Test St',
            'city': 'Test City',
            'state': 'Test State',
            'country': 'Test Country',
            'postal_code': '12345',
            'capacity': 100,
            'owner_id': self.owner_id,
        }
        venue = self.service.execute(data)
        self.assertIsNotNone(venue.id)
        self.assertEqual(venue.name, 'Test Venue')


class UpdateVenueServiceTest(TestCase):
    """Tests for UpdateVenueService."""
    
    def setUp(self):
        self.service = UpdateVenueService()
        self.owner_id = uuid.uuid4()
        self.venue = Venue.objects.create(
            name='Original Name',
            address='123 Test St',
            city='Test City',
            state='Test State',
            country='Test Country',
            postal_code='12345',
            capacity=100,
            owner_id=self.owner_id,
        )
        
    def test_update_venue(self):
        """Test updating a venue."""
        data = {'name': 'Updated Name'}
        updated = self.service.execute(self.venue.id, data)
        self.assertEqual(updated.name, 'Updated Name')


class SearchVenueServiceTest(TestCase):
    """Tests for SearchVenueService."""
    
    def setUp(self):
        self.service = SearchVenueService()
        self.owner_id = uuid.uuid4()
        
    def test_search_by_city(self):
        """Test searching venues by city."""
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
        venues = self.service.execute(city='New York')
        self.assertEqual(len(venues), 1)
        self.assertEqual(venues[0].city, 'New York')


class GetVenueServiceTest(TestCase):
    """Tests for GetVenueService."""
    
    def setUp(self):
        self.service = GetVenueService()
        self.owner_id = uuid.uuid4()
        self.venue = Venue.objects.create(
            name='Test Venue',
            address='123 Test St',
            city='Test City',
            state='Test State',
            country='Test Country',
            postal_code='12345',
            capacity=100,
            owner_id=self.owner_id,
        )
        
    def test_get_venue(self):
        """Test getting a venue."""
        venue = self.service.execute(self.venue.id)
        self.assertEqual(venue.id, self.venue.id)
        
    def test_get_nonexistent_venue(self):
        """Test getting non-existent venue."""
        with self.assertRaises(ValidationError):
            self.service.execute(uuid.uuid4())
