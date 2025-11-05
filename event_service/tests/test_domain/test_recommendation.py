import uuid
from django.test import TestCase

from domain.recommendation import UserPreference, RecommendationScore


class UserPreferenceModelTest(TestCase):
    """Tests for UserPreference model."""
    
    def test_create_preference(self):
        """Test creating user preference."""
        pref = UserPreference.objects.create(
            user_id=uuid.uuid4(),
            preferred_categories=['Technology', 'Music'],
            preferred_tags=['python', 'django'],
        )
        self.assertIsNotNone(pref.id)
        
    def test_add_viewed_event(self):
        """Test adding viewed event."""
        pref = UserPreference.objects.create(user_id=uuid.uuid4())
        event_id = uuid.uuid4()
        
        pref.add_viewed_event(event_id)
        
        pref.refresh_from_db()
        self.assertIn(str(event_id), pref.viewed_events)
        
    def test_add_registered_event(self):
        """Test adding registered event."""
        pref = UserPreference.objects.create(user_id=uuid.uuid4())
        event_id = uuid.uuid4()
        
        pref.add_registered_event(event_id)
        
        pref.refresh_from_db()
        self.assertIn(str(event_id), pref.registered_events)


class RecommendationScoreModelTest(TestCase):
    """Tests for RecommendationScore model."""
    
    def test_create_score(self):
        """Test creating recommendation score."""
        score = RecommendationScore.objects.create(
            user_id=uuid.uuid4(),
            event_id=uuid.uuid4(),
            category_score=0.8,
            tag_score=0.6,
        )
        self.assertIsNotNone(score.id)
        
    def test_calculate_total_score(self):
        """Test total score calculation."""
        score = RecommendationScore(
            user_id=uuid.uuid4(),
            event_id=uuid.uuid4(),
            category_score=1.0,
            tag_score=0.8,
            location_score=0.6,
            popularity_score=0.4,
        )
        total = score.calculate_total_score()
        
        # 1.0*0.3 + 0.8*0.25 + 0.6*0.25 + 0.4*0.2 = 0.3 + 0.2 + 0.15 + 0.08 = 0.73
        self.assertAlmostEqual(total, 0.73, places=2)
