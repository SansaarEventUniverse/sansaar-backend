import uuid
import json
from django.test import TestCase, Client

from domain.search_index import EventSearchIndex
from domain.category import Category, Tag
from domain.location import EventLocation
from domain.recommendation import UserPreference


class SearchWorkflowE2ETest(TestCase):
    """End-to-end tests for complete search workflows."""
    
    def setUp(self):
        self.client = Client()
        
        # Create test data
        Category.objects.create(name='Technology', slug='technology')
        Tag.objects.create(name='python', slug='python')
        
        EventSearchIndex.objects.create(
            event_id=uuid.uuid4(),
            title='Python Conference 2026',
            description='Annual Python conference',
            category='Technology',
            tags=['python', 'conference'],
            city='San Francisco',
            is_published=True,
            search_rank=15.0,
        )
        
    def test_complete_search_workflow(self):
        """Test complete search workflow from query to results."""
        # Step 1: Search for events
        response = self.client.get('/api/events/search/?q=Python')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['count'], 1)
        
        # Step 2: Get search filters
        response = self.client.get('/api/events/search/filters/')
        self.assertEqual(response.status_code, 200)
        filters = response.json()
        self.assertIn('Technology', filters['categories'])
        
        # Step 3: Search with filters
        response = self.client.get('/api/events/search/?category=Technology')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 1)


class RecommendationWorkflowE2ETest(TestCase):
    """End-to-end tests for recommendation workflows."""
    
    def setUp(self):
        self.client = Client()
        self.user_id = uuid.uuid4()
        
        EventSearchIndex.objects.create(
            event_id=uuid.uuid4(),
            title='Python Conference',
            category='Technology',
            tags=['python'],
            is_published=True,
        )
        
    def test_complete_recommendation_workflow(self):
        """Test complete recommendation workflow."""
        # Step 1: Create user preferences
        response = self.client.post(
            f'/api/events/users/{self.user_id}/preferences/',
            data=json.dumps({
                'preferred_categories': ['Technology'],
                'preferred_tags': ['python'],
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        
        # Step 2: Get recommendations
        response = self.client.get(
            f'/api/events/recommendations/?user_id={self.user_id}'
        )
        self.assertEqual(response.status_code, 200)
        recommendations = response.json()['recommendations']
        self.assertGreater(len(recommendations), 0)
        
        # Step 3: Get similar events
        event_id = recommendations[0]['event_id']
        response = self.client.get(f'/api/events/{event_id}/similar/')
        self.assertEqual(response.status_code, 200)


class LocationSearchWorkflowE2ETest(TestCase):
    """End-to-end tests for location search workflows."""
    
    def setUp(self):
        self.client = Client()
        
        EventLocation.objects.create(
            event_id=uuid.uuid4(),
            address='123 Main St',
            city='San Francisco',
            country='USA',
            latitude=37.7749,
            longitude=-122.4194,
        )
        
    def test_complete_location_search_workflow(self):
        """Test complete location search workflow."""
        # Step 1: Search nearby
        response = self.client.get(
            '/api/events/nearby/?latitude=37.7749&longitude=-122.4194&radius_km=10'
        )
        self.assertEqual(response.status_code, 200)
        self.assertGreater(response.json()['count'], 0)
        
        # Step 2: Search by city
        response = self.client.get('/api/events/search/location/?city=San Francisco')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 1)
        
        # Step 3: Get map events
        response = self.client.get(
            '/api/events/map/?min_lat=37.0&max_lat=38.0&min_lon=-123.0&max_lon=-122.0'
        )
        self.assertEqual(response.status_code, 200)
        self.assertGreater(response.json()['count'], 0)
