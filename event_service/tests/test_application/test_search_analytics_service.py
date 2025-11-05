from django.test import TestCase

from domain.search_analytics import SearchQuery
from application.search_analytics_service import (
    SearchAnalyticsService,
    QueryAnalysisService,
    SearchOptimizationService,
)


class SearchAnalyticsServiceTest(TestCase):
    """Tests for SearchAnalyticsService."""
    
    def test_track_search(self):
        """Test tracking a search."""
        service = SearchAnalyticsService()
        query = service.track_search(
            query_text='python',
            result_count=10,
            response_time_ms=150,
        )
        self.assertIsNotNone(query.id)
        
    def test_get_analytics(self):
        """Test getting analytics."""
        service = SearchAnalyticsService()
        service.track_search('python', 10, 100)
        service.track_search('django', 5, 150)
        
        analytics = service.get_analytics(days=7)
        
        self.assertEqual(analytics['total_searches'], 2)
        self.assertEqual(analytics['unique_queries'], 2)


class QueryAnalysisServiceTest(TestCase):
    """Tests for QueryAnalysisService."""
    
    def test_get_popular_searches(self):
        """Test getting popular searches."""
        SearchQuery.objects.create(query_text='python', result_count=10)
        SearchQuery.objects.create(query_text='python', result_count=8)
        SearchQuery.objects.create(query_text='django', result_count=5)
        
        service = QueryAnalysisService()
        popular = service.get_popular_searches(limit=10)
        
        self.assertEqual(len(popular), 2)
        self.assertEqual(popular[0]['query_text'], 'python')
        self.assertEqual(popular[0]['count'], 2)


class SearchOptimizationServiceTest(TestCase):
    """Tests for SearchOptimizationService."""
    
    def test_get_performance_metrics(self):
        """Test getting performance metrics."""
        SearchQuery.objects.create(
            query_text='slow query',
            result_count=10,
            response_time_ms=600,
        )
        SearchQuery.objects.create(
            query_text='fast query',
            result_count=10,
            response_time_ms=50,
        )
        
        service = SearchOptimizationService()
        metrics = service.get_performance_metrics()
        
        self.assertIn('avg_response_time', metrics)
        self.assertEqual(len(metrics['slow_queries']), 1)
        self.assertEqual(len(metrics['fast_queries']), 1)
