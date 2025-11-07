import uuid
import time
from django.test import TestCase

from domain.search_index import EventSearchIndex
from domain.recommendation import UserPreference
from application.search_service import EventSearchService
from application.recommendation_service import EventRecommendationService
from application.search_analytics_service import SearchAnalyticsService


class SearchPerformanceTest(TestCase):
    """Performance tests for search functionality."""
    
    def test_search_response_time(self):
        """Test search response time with large dataset."""
        # Create 100 events
        for i in range(100):
            EventSearchIndex.objects.create(
                event_id=uuid.uuid4(),
                title=f'Event {i}',
                description=f'Description {i}',
                category='Technology' if i % 2 == 0 else 'Music',
                is_published=True,
            )
        
        service = EventSearchService()
        
        # Measure search time
        start = time.time()
        results = service.execute('Event', {})
        duration = time.time() - start
        
        # Should complete in under 1 second
        self.assertLess(duration, 1.0)
        self.assertGreater(len(results), 0)


class RecommendationPerformanceTest(TestCase):
    """Performance tests for recommendation generation."""
    
    def test_recommendation_generation_time(self):
        """Test recommendation generation performance."""
        user_id = uuid.uuid4()
        
        # Create user preferences
        UserPreference.objects.create(
            user_id=user_id,
            preferred_categories=['Technology'],
            preferred_tags=['python'],
        )
        
        # Create 50 events
        for i in range(50):
            EventSearchIndex.objects.create(
                event_id=uuid.uuid4(),
                title=f'Tech Event {i}',
                category='Technology',
                tags=['python', 'conference'],
                is_published=True,
            )
        
        service = EventRecommendationService()
        
        # Measure recommendation time
        start = time.time()
        recommendations = service.generate_recommendations(user_id, limit=10)
        duration = time.time() - start
        
        # Should complete in under 0.5 seconds
        self.assertLess(duration, 0.5)
        self.assertEqual(len(recommendations), 10)


class AnalyticsPerformanceTest(TestCase):
    """Performance tests for analytics processing."""
    
    def test_analytics_aggregation_performance(self):
        """Test analytics aggregation with large query volume."""
        service = SearchAnalyticsService()
        
        # Track 100 searches
        for i in range(100):
            service.track_search(
                query_text=f'query {i % 10}',
                result_count=i % 20,
                response_time_ms=100 + (i % 50),
            )
        
        # Measure analytics generation time
        start = time.time()
        analytics = service.get_analytics(days=7)
        duration = time.time() - start
        
        # Should complete in under 0.5 seconds
        self.assertLess(duration, 0.5)
        self.assertEqual(analytics['total_searches'], 100)
