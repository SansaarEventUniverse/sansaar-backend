import uuid
import json
from django.test import TestCase, Client

from domain.recommendation import UserPreference
from domain.search_index import EventSearchIndex


class RecommendationAPITest(TestCase):
    """Tests for Recommendation API endpoints."""
    
    def setUp(self):
        self.client = Client()
        self.user_id = uuid.uuid4()
        
        UserPreference.objects.create(
            user_id=self.user_id,
            preferred_categories=['Technology'],
            preferred_tags=['python'],
        )
        
        EventSearchIndex.objects.create(
            event_id=uuid.uuid4(),
            title='Python Conference',
            description='Python event',
            category='Technology',
            tags=['python'],
            is_published=True,
        )
        
    def test_get_recommendations(self):
        """Test getting recommendations via API."""
        response = self.client.get(
            f'/api/events/recommendations/?user_id={self.user_id}'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('recommendations', data)
        
    def test_get_preferences(self):
        """Test getting user preferences via API."""
        response = self.client.get(
            f'/api/events/users/{self.user_id}/preferences/'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['preferred_categories'], ['Technology'])
        
    def test_update_preferences(self):
        """Test updating preferences via API."""
        data = {
            'preferred_categories': ['Music', 'Technology'],
            'preferred_tags': ['django', 'python'],
        }
        response = self.client.post(
            f'/api/events/users/{self.user_id}/preferences/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn('Music', result['preferred_categories'])
        
    def test_get_similar_events(self):
        """Test getting similar events via API."""
        event = EventSearchIndex.objects.create(
            event_id=uuid.uuid4(),
            title='Django Conference',
            category='Technology',
            is_published=True,
        )
        EventSearchIndex.objects.create(
            event_id=uuid.uuid4(),
            title='Tech Meetup',
            category='Technology',
            is_published=True,
        )
        
        response = self.client.get(
            f'/api/events/{event.event_id}/similar/'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('similar_events', data)
