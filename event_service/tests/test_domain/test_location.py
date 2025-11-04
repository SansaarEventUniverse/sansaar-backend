import uuid
from django.test import TestCase

from domain.location import LocationSearch, EventLocation


class LocationSearchModelTest(TestCase):
    """Tests for LocationSearch model."""
    
    def test_create_location_search(self):
        """Test creating location search."""
        search = LocationSearch.objects.create(
            latitude=37.7749,
            longitude=-122.4194,
            radius_km=10.0,
            city='San Francisco',
        )
        self.assertIsNotNone(search.id)
        
    def test_calculate_distance(self):
        """Test distance calculation."""
        # SF to LA (approx 559 km)
        distance = LocationSearch.calculate_distance(
            37.7749, -122.4194,  # San Francisco
            34.0522, -118.2437   # Los Angeles
        )
        self.assertAlmostEqual(distance, 559, delta=10)


class EventLocationModelTest(TestCase):
    """Tests for EventLocation model."""
    
    def test_create_event_location(self):
        """Test creating event location."""
        location = EventLocation.objects.create(
            event_id=uuid.uuid4(),
            address='123 Main St',
            city='San Francisco',
            country='USA',
            latitude=37.7749,
            longitude=-122.4194,
        )
        self.assertIsNotNone(location.id)
        
    def test_distance_to(self):
        """Test distance calculation to coordinates."""
        location = EventLocation.objects.create(
            event_id=uuid.uuid4(),
            address='123 Main St',
            city='San Francisco',
            country='USA',
            latitude=37.7749,
            longitude=-122.4194,
        )
        
        # Distance to LA
        distance = location.distance_to(34.0522, -118.2437)
        self.assertAlmostEqual(distance, 559, delta=10)
