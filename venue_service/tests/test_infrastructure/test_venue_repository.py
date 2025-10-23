import uuid
from django.test import TestCase

from infrastructure.repositories.venue_repository import VenueRepository
from domain.venue import Venue


class VenueRepositoryTest(TestCase):
    """Tests for VenueRepository."""
    
    def setUp(self):
        self.repository = VenueRepository()
        self.owner_id = uuid.uuid4()
        
    def test_get_owner_venues(self):
        """Test getting owner venues."""
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
        venues = self.repository.get_owner_venues(self.owner_id)
        self.assertEqual(len(venues), 1)
        self.assertEqual(venues[0].id, venue.id)
        
    def test_search_by_location(self):
        """Test searching by location."""
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
        venues = self.repository.search_by_location(city='New York')
        self.assertEqual(len(venues), 1)
        
    def test_get_verified_venues(self):
        """Test getting verified venues."""
        venue = Venue.objects.create(
            name='Verified Venue',
            address='123 Test St',
            city='Test City',
            state='Test State',
            country='Test Country',
            postal_code='12345',
            capacity=100,
            owner_id=self.owner_id,
        )
        venue.verify()
        
        venues = self.repository.get_verified_venues()
        self.assertEqual(len(venues), 1)
        self.assertTrue(venues[0].is_verified)
