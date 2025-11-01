import uuid
from django.test import TestCase

from infrastructure.services.analytics_cache_service import AnalyticsCacheService


class AnalyticsCacheServiceTest(TestCase):
    """Tests for AnalyticsCacheService."""
    
    def test_cache_and_retrieve(self):
        """Test caching and retrieving analytics."""
        service = AnalyticsCacheService()
        event_id = uuid.uuid4()
        data = {'total': 100, 'confirmed': 80}
        
        service.cache_analytics(event_id, data)
        cached = service.get_cached_analytics(event_id)
        
        self.assertIsNotNone(cached)
        self.assertEqual(cached['total'], 100)
        
    def test_invalidate_cache(self):
        """Test cache invalidation."""
        service = AnalyticsCacheService()
        event_id = uuid.uuid4()
        data = {'total': 100}
        
        service.cache_analytics(event_id, data)
        service.invalidate_cache(event_id)
        cached = service.get_cached_analytics(event_id)
        
        self.assertIsNone(cached)
