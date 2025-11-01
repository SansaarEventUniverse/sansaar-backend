import uuid
from django.test import TestCase

from domain.search_index import EventSearchIndex
from application.search_service import (
    EventSearchService,
    SearchFilterService,
    SearchRankingService,
)


class EventSearchServiceTest(TestCase):
    """Tests for EventSearchService."""
    
    def setUp(self):
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
        
    def test_search_by_query(self):
        """Test searching events by query."""
        service = EventSearchService()
        results = service.execute('Tech')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, 'Tech Conference 2026')
        
    def test_search_with_filters(self):
        """Test searching with filters."""
        service = EventSearchService()
        results = service.execute('', {'category': 'Music'})
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].category, 'Music')


class SearchFilterServiceTest(TestCase):
    """Tests for SearchFilterService."""
    
    def test_get_filters(self):
        """Test getting available filters."""
        EventSearchIndex.objects.create(
            event_id=uuid.uuid4(),
            title='Test Event',
            description='Test',
            category='Technology',
            city='New York',
            is_published=True,
        )
        
        service = SearchFilterService()
        filters = service.execute()
        
        self.assertIn('categories', filters)
        self.assertIn('cities', filters)
        self.assertIn('Technology', filters['categories'])
        self.assertIn('New York', filters['cities'])


class SearchRankingServiceTest(TestCase):
    """Tests for SearchRankingService."""
    
    def test_update_ranking(self):
        """Test updating search ranking."""
        event_id = uuid.uuid4()
        EventSearchIndex.objects.create(
            event_id=event_id,
            title='Test Event',
            description='Test',
            is_published=True,
            view_count=10,
        )
        
        service = SearchRankingService()
        index = service.execute(event_id)
        
        self.assertIsNotNone(index)
        self.assertEqual(index.search_rank, 11.0)  # 10 + 1
        
    def test_increment_view_count(self):
        """Test incrementing view count."""
        event_id = uuid.uuid4()
        index = EventSearchIndex.objects.create(
            event_id=event_id,
            title='Test Event',
            description='Test',
            is_published=True,
            view_count=5,
        )
        
        service = SearchRankingService()
        service.increment_view_count(event_id)
        
        index.refresh_from_db()
        self.assertEqual(index.view_count, 6)
