import uuid
from django.test import TestCase

from domain.search_index import EventSearchIndex
from infrastructure.services.search_cache_service import SearchCacheService


class SearchCacheServiceTest(TestCase):
    """Tests for SearchCacheService."""
    
    def test_cache_and_retrieve_results(self):
        """Test caching and retrieving search results."""
        service = SearchCacheService()
        
        # Create test data
        index = EventSearchIndex.objects.create(
            event_id=uuid.uuid4(),
            title='Test Event',
            description='Test description',
            category='Technology',
            is_published=True,
        )
        
        # Cache results
        service.cache_results('test', {}, [index])
        
        # Retrieve cached results
        cached = service.get_cached_results('test', {})
        
        self.assertIsNotNone(cached)
        self.assertEqual(len(cached), 1)
        self.assertEqual(cached[0]['title'], 'Test Event')
        
    def test_cache_with_filters(self):
        """Test caching with filters."""
        service = SearchCacheService()
        index = EventSearchIndex.objects.create(
            event_id=uuid.uuid4(),
            title='Tech Event',
            description='Test',
            category='Technology',
            is_published=True,
        )
        
        filters = {'category': 'Technology'}
        service.cache_results('tech', filters, [index])
        
        cached = service.get_cached_results('tech', filters)
        self.assertIsNotNone(cached)
        
    def test_invalidate_cache(self):
        """Test cache invalidation."""
        service = SearchCacheService()
        index = EventSearchIndex.objects.create(
            event_id=uuid.uuid4(),
            title='Test Event',
            description='Test',
            is_published=True,
        )
        
        service.cache_results('test', {}, [index])
        service.invalidate_cache('test')
        
        cached = service.get_cached_results('test', {})
        self.assertIsNone(cached)
