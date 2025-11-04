import uuid
from django.test import TestCase

from domain.location import EventLocation
from application.location_service import (
    LocationSearchService,
    NearbyEventsService,
    GeoFilterService,
)


class LocationSearchServiceTest(TestCase):
    """Tests for LocationSearchService."""
    
    def setUp(self):
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
        """Test searching nearby events."""
        service = LocationSearchService()
        # Search from SF coordinates
        nearby = service.search_nearby(37.7749, -122.4194, radius_km=20.0)
        
        self.assertEqual(len(nearby), 2)
        self.assertLess(nearby[0]['distance_km'], nearby[1]['distance_km'])


class NearbyEventsServiceTest(TestCase):
    """Tests for NearbyEventsService."""
    
    def test_find_nearby_events(self):
        """Test finding events near a city."""
        EventLocation.objects.create(
            event_id=uuid.uuid4(),
            address='123 Main St',
            city='San Francisco',
            country='USA',
            latitude=37.7749,
            longitude=-122.4194,
        )
        
        service = NearbyEventsService()
        nearby = service.execute('San Francisco', radius_km=50.0)
        
        self.assertGreaterEqual(len(nearby), 1)


class GeoFilterServiceTest(TestCase):
    """Tests for GeoFilterService."""
    
    def test_filter_by_city(self):
        """Test filtering by city."""
        EventLocation.objects.create(
            event_id=uuid.uuid4(),
            address='123 Main St',
            city='San Francisco',
            country='USA',
            latitude=37.7749,
            longitude=-122.4194,
        )
        
        service = GeoFilterService()
        results = service.filter_by_city('San Francisco')
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].city, 'San Francisco')
