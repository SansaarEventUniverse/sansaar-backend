import uuid
from django.test import TestCase

from domain.search_index import EventSearchIndex


class EventSearchIndexModelTest(TestCase):
    """Tests for EventSearchIndex model."""
    
    def test_create_search_index(self):
        """Test creating search index entry."""
        index = EventSearchIndex.objects.create(
            event_id=uuid.uuid4(),
            title='Tech Conference 2026',
            description='Annual tech conference',
            category='Technology',
            is_published=True,
        )
        self.assertIsNotNone(index.id)
        
    def test_calculate_rank(self):
        """Test rank calculation."""
        index = EventSearchIndex(
            event_id=uuid.uuid4(),
            title='Test Event',
            description='Test',
            is_published=True,
            view_count=100,
            tags=['tech', 'conference'],
        )
        rank = index.calculate_rank()
        # 10 (published) + 10 (100 views * 0.1) + 1 (2 tags * 0.5) = 21
        self.assertEqual(rank, 21.0)
        
    def test_update_rank(self):
        """Test rank update."""
        index = EventSearchIndex.objects.create(
            event_id=uuid.uuid4(),
            title='Test Event',
            description='Test',
            is_published=True,
            view_count=50,
        )
        index.update_rank()
        self.assertEqual(index.search_rank, 15.0)  # 10 + 5
