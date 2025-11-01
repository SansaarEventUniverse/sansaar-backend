import uuid
import json
from typing import Dict, Any
from django.core.cache import cache


class AnalyticsCacheService:
    """Service for caching analytics data."""
    
    CACHE_TIMEOUT = 300  # 5 minutes
    
    def cache_analytics(self, event_id: uuid.UUID, data: Dict[str, Any]) -> None:
        """Cache analytics data."""
        key = f"analytics:{event_id}"
        cache.set(key, json.dumps(data), timeout=self.CACHE_TIMEOUT)
    
    def get_cached_analytics(self, event_id: uuid.UUID) -> Dict[str, Any]:
        """Get cached analytics data."""
        key = f"analytics:{event_id}"
        data = cache.get(key)
        if data:
            return json.loads(data)
        return None
    
    def invalidate_cache(self, event_id: uuid.UUID) -> None:
        """Invalidate analytics cache."""
        key = f"analytics:{event_id}"
        cache.delete(key)
