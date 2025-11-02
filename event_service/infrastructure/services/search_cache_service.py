import json
from typing import List, Dict, Any
from django.core.cache import cache

from domain.search_index import EventSearchIndex


class SearchCacheService:
    """Service for caching search results."""
    
    CACHE_TIMEOUT = 300  # 5 minutes
    
    def cache_results(self, query: str, filters: Dict[str, Any], 
                     results: List[EventSearchIndex]) -> None:
        """Cache search results."""
        key = self._generate_key(query, filters)
        data = [
            {
                'event_id': str(r.event_id),
                'title': r.title,
                'description': r.description,
                'category': r.category,
                'city': r.city,
                'search_rank': r.search_rank,
            }
            for r in results
        ]
        cache.set(key, json.dumps(data), timeout=self.CACHE_TIMEOUT)
    
    def get_cached_results(self, query: str, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get cached search results."""
        key = self._generate_key(query, filters)
        data = cache.get(key)
        if data:
            return json.loads(data)
        return None
    
    def invalidate_cache(self, query: str = None) -> None:
        """Invalidate search cache."""
        if query:
            # Invalidate specific query
            key = self._generate_key(query, {})
            cache.delete(key)
        else:
            # Clear all search cache (would need pattern matching in production)
            pass
    
    def _generate_key(self, query: str, filters: Dict[str, Any]) -> str:
        """Generate cache key."""
        filter_str = json.dumps(filters, sort_keys=True) if filters else ''
        return f"search:{query}:{filter_str}"
