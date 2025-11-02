import uuid
from django.test import TestCase, Client

from domain.search_index import EventSearchIndex


class SearchAPITest(TestCase):
    """Tests for Search API endpoints."""
    
    def setUp(self):
        self.client = Client()
        
        EventSearchIndex.objects.create(
            event_id=uuid.uuid4(),
            title='Tech Conference 2026',
            description='Annual technology conference',
            category='Technology',
            city='San Francisco',
            is_published=True,
            search_rank=10.0,
        )
        EventSearchIndex.objects.create(
            event_id=uuid.uuid4(),
            title='Music Festival',
            description='Summer music event',
            category='Music',
            city='Los Angeles',
            is_published=True,
            search_rank=5.0,
        )
        
    def test_search_events(self):
        """Test searching events via API."""
        response = self.client.get('/api/events/search/?q=Tech')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('results', data)
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['results'][0]['title'], 'Tech Conference 2026')
        
    def test_search_with_filters(self):
        """Test searching with filters via API."""
        response = self.client.get('/api/events/search/?category=Music')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['results'][0]['category'], 'Music')
        
    def test_get_search_filters(self):
        """Test getting search filters via API."""
        response = self.client.get('/api/events/search/filters/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('categories', data)
        self.assertIn('cities', data)
        self.assertIn('Technology', data['categories'])
        
    def test_get_search_suggestions(self):
        """Test getting search suggestions via API."""
        response = self.client.get('/api/events/search/suggestions/?q=Tech')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('suggestions', data)
        self.assertEqual(len(data['suggestions']), 1)
        self.assertEqual(data['suggestions'][0]['title'], 'Tech Conference 2026')
        
    def test_search_caching(self):
        """Test search result caching."""
        # First request
        response1 = self.client.get('/api/events/search/?q=Tech')
        self.assertFalse(response1.json()['cached'])
        
        # Second request (should be cached)
        response2 = self.client.get('/api/events/search/?q=Tech')
        self.assertTrue(response2.json()['cached'])
