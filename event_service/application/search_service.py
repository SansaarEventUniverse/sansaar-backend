from typing import Dict, Any, List
import uuid
from django.db.models import Q
from django.contrib.postgres.search import SearchQuery, SearchRank

from domain.search_index import EventSearchIndex


class EventSearchService:
    """Service for searching events."""
    
    def execute(self, query: str, filters: Dict[str, Any] = None) -> List[EventSearchIndex]:
        """Search events with query and filters."""
        results = EventSearchIndex.objects.filter(is_published=True)
        
        # Apply text search
        if query:
            search_query = SearchQuery(query)
            results = results.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(category__icontains=query)
            )
        
        # Apply filters
        if filters:
            if 'category' in filters:
                results = results.filter(category=filters['category'])
            if 'city' in filters:
                results = results.filter(city=filters['city'])
            if 'status' in filters:
                results = results.filter(status=filters['status'])
        
        # Order by rank
        return results.order_by('-search_rank', '-created_at')[:50]


class SearchFilterService:
    """Service for getting available search filters."""
    
    def execute(self) -> Dict[str, List[str]]:
        """Get available filter options."""
        published_events = EventSearchIndex.objects.filter(is_published=True)
        
        categories = list(
            published_events.values_list('category', flat=True)
            .distinct()
            .exclude(category='')
        )
        
        cities = list(
            published_events.values_list('city', flat=True)
            .distinct()
            .exclude(city='')
        )
        
        return {
            'categories': categories,
            'cities': cities,
            'statuses': ['published', 'upcoming', 'ongoing'],
        }


class SearchRankingService:
    """Service for updating search rankings."""
    
    def execute(self, event_id: uuid.UUID) -> EventSearchIndex:
        """Update search ranking for an event."""
        try:
            index = EventSearchIndex.objects.get(event_id=event_id)
            index.update_rank()
            index.save()
            return index
        except EventSearchIndex.DoesNotExist:
            return None
    
    def increment_view_count(self, event_id: uuid.UUID) -> None:
        """Increment view count and update rank."""
        try:
            index = EventSearchIndex.objects.get(event_id=event_id)
            index.view_count += 1
            index.update_rank()
            index.save()
        except EventSearchIndex.DoesNotExist:
            pass
