from django.test import TestCase, Client

from domain.search_analytics import SearchQuery


class SearchAnalyticsAPITest(TestCase):
    """Tests for Search Analytics API endpoints."""
    
    def setUp(self):
        self.client = Client()
        
        SearchQuery.objects.create(
            query_text='python',
            result_count=10,
            response_time_ms=100,
        )
        SearchQuery.objects.create(
            query_text='python',
            result_count=8,
            response_time_ms=150,
        )
        SearchQuery.objects.create(
            query_text='django',
            result_count=0,
            response_time_ms=50,
        )
        
    def test_get_search_analytics(self):
        """Test getting search analytics via API."""
        response = self.client.get('/api/events/search/analytics/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('total_searches', data)
        self.assertEqual(data['total_searches'], 3)
        self.assertEqual(data['unique_queries'], 2)
        
    def test_get_search_performance(self):
        """Test getting search performance via API."""
        response = self.client.get('/api/events/search/performance/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('avg_response_time', data)
        self.assertIn('slow_queries', data)
        self.assertIn('fast_queries', data)
        
    def test_get_popular_searches(self):
        """Test getting popular searches via API."""
        response = self.client.get('/api/events/search/popular/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('popular_searches', data)
        self.assertEqual(len(data['popular_searches']), 2)
        self.assertEqual(data['popular_searches'][0]['query_text'], 'python')
        self.assertEqual(data['popular_searches'][0]['count'], 2)
