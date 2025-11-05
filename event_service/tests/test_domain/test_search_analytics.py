import uuid
from datetime import date
from django.test import TestCase

from domain.search_analytics import SearchQuery, SearchAnalytics


class SearchQueryModelTest(TestCase):
    """Tests for SearchQuery model."""
    
    def test_create_search_query(self):
        """Test creating search query."""
        query = SearchQuery.objects.create(
            query_text='python conference',
            result_count=10,
            response_time_ms=150,
        )
        self.assertIsNotNone(query.id)
        
    def test_query_with_filters(self):
        """Test query with filters."""
        query = SearchQuery.objects.create(
            query_text='tech events',
            filters={'category': 'Technology', 'city': 'SF'},
            result_count=5,
        )
        self.assertEqual(query.filters['category'], 'Technology')


class SearchAnalyticsModelTest(TestCase):
    """Tests for SearchAnalytics model."""
    
    def test_create_analytics(self):
        """Test creating analytics."""
        analytics = SearchAnalytics.objects.create(
            date=date.today(),
            total_searches=100,
            unique_queries=50,
        )
        self.assertIsNotNone(analytics.id)
        
    def test_calculate_metrics(self):
        """Test metrics calculation."""
        queries = [
            SearchQuery.objects.create(
                query_text='python',
                result_count=10,
                response_time_ms=100,
            ),
            SearchQuery.objects.create(
                query_text='python',
                result_count=8,
                response_time_ms=150,
            ),
            SearchQuery.objects.create(
                query_text='django',
                result_count=0,
                response_time_ms=50,
            ),
        ]
        
        analytics = SearchAnalytics(date=date.today())
        analytics.calculate_metrics(queries)
        
        self.assertEqual(analytics.total_searches, 3)
        self.assertEqual(analytics.unique_queries, 2)
        self.assertEqual(analytics.avg_response_time_ms, 100.0)
        self.assertEqual(len(analytics.popular_queries), 2)
        self.assertIn('django', analytics.zero_result_queries)
