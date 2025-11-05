import uuid
from django.test import TestCase

from domain.recommendation import UserPreference
from domain.search_index import EventSearchIndex
from application.recommendation_service import (
    UserPreferenceService,
    EventRecommendationService,
    SimilarEventsService,
)


class UserPreferenceServiceTest(TestCase):
    """Tests for UserPreferenceService."""
    
    def test_get_or_create_preference(self):
        """Test getting or creating preference."""
        service = UserPreferenceService()
        user_id = uuid.uuid4()
        
        pref = service.get_or_create_preference(user_id)
        self.assertIsNotNone(pref.id)
        
    def test_update_preferences(self):
        """Test updating preferences."""
        service = UserPreferenceService()
        user_id = uuid.uuid4()
        
        pref = service.update_preferences(user_id, {
            'preferred_categories': ['Technology'],
            'preferred_tags': ['python'],
        })
        
        self.assertEqual(pref.preferred_categories, ['Technology'])


class EventRecommendationServiceTest(TestCase):
    """Tests for EventRecommendationService."""
    
    def setUp(self):
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
            tags=['python', 'conference'],
            is_published=True,
            search_rank=10.0,
        )
        
    def test_generate_recommendations(self):
        """Test generating recommendations."""
        service = EventRecommendationService()
        recommendations = service.generate_recommendations(self.user_id, limit=10)
        
        self.assertGreaterEqual(len(recommendations), 1)
        self.assertIn('event_id', recommendations[0])
        self.assertIn('score', recommendations[0])


class SimilarEventsServiceTest(TestCase):
    """Tests for SimilarEventsService."""
    
    def test_find_similar(self):
        """Test finding similar events."""
        event1 = EventSearchIndex.objects.create(
            event_id=uuid.uuid4(),
            title='Python Conference',
            category='Technology',
            is_published=True,
        )
        EventSearchIndex.objects.create(
            event_id=uuid.uuid4(),
            title='Django Meetup',
            category='Technology',
            is_published=True,
        )
        
        service = SimilarEventsService()
        similar = service.find_similar(event1.event_id, limit=5)
        
        self.assertEqual(len(similar), 1)
