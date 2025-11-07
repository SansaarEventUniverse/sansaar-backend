import uuid
from django.test import TestCase

from domain.search_index import EventSearchIndex
from domain.category import Category, Tag
from domain.location import EventLocation
from application.search_service import EventSearchService
from application.category_service import EventCategorizationService


class SearchIntegrationTest(TestCase):
    """Integration tests for search functionality."""
    
    def test_full_text_search_with_filters(self):
        """Test full-text search with category and location filters."""
        # Create categories and tags
        Category.objects.create(name='Technology', slug='technology')
        Tag.objects.create(name='python', slug='python')
        
        # Create events
        event1 = EventSearchIndex.objects.create(
            event_id=uuid.uuid4(),
            title='Python Conference 2026',
            description='Annual Python conference',
            category='Technology',
            tags=['python', 'conference'],
            city='San Francisco',
            is_published=True,
            search_rank=15.0,
        )
        
        EventSearchIndex.objects.create(
            event_id=uuid.uuid4(),
            title='Music Festival',
            description='Summer music event',
            category='Music',
            city='Los Angeles',
            is_published=True,
            search_rank=10.0,
        )
        
        # Search with filters
        service = EventSearchService()
        results = service.execute('Python', {'category': 'Technology'})
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, 'Python Conference 2026')


class CategoryIntegrationTest(TestCase):
    """Integration tests for category management."""
    
    def test_category_hierarchy_with_events(self):
        """Test category hierarchy with event assignment."""
        # Create hierarchy
        parent = Category.objects.create(name='Technology', slug='technology')
        child = Category.objects.create(
            name='AI & ML',
            slug='ai-ml',
            parent=parent
        )
        
        # Assign events to categories
        service = EventCategorizationService()
        event_id = uuid.uuid4()
        
        service.assign_category(event_id, child.id)
        
        child.refresh_from_db()
        self.assertEqual(child.event_count, 1)
        
        # Verify hierarchy
        ancestors = child.get_ancestors()
        self.assertIn(parent, ancestors)


class LocationSearchIntegrationTest(TestCase):
    """Integration tests for location-based search."""
    
    def test_nearby_search_with_distance_calculation(self):
        """Test nearby search with accurate distance calculation."""
        # Create locations
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
        
        # Search nearby
        from application.location_service import LocationSearchService
        service = LocationSearchService()
        
        results = service.search_nearby(37.7749, -122.4194, radius_km=20.0)
        
        self.assertEqual(len(results), 2)
        self.assertLess(results[0]['distance_km'], results[1]['distance_km'])
