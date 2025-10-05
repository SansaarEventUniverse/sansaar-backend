import json
from infrastructure.cache.cache_service import CacheService


class PermissionCacheService:
    def __init__(self):
        self.cache = CacheService()
        self.prefix = 'permission'

    def _get_key(self, event_id, user_id):
        return f"{self.prefix}:{event_id}:{user_id}"

    def cache_permission(self, event_id, user_id, has_permission):
        key = self._get_key(event_id, user_id)
        self.cache.set(key, json.dumps(has_permission))

    def get_cached_permission(self, event_id, user_id):
        key = self._get_key(event_id, user_id)
        value = self.cache.get(key)
        if value is not None:
            return json.loads(value)
        return None

    def invalidate_user_cache(self, event_id, user_id):
        key = self._get_key(event_id, user_id)
        self.cache.delete(key)

    def invalidate_event_cache(self, event_id):
        pattern = f"{self.prefix}:{event_id}:*"
        self.cache.clear_pattern(pattern)

    def clear_all(self):
        pattern = f"{self.prefix}:*"
        self.cache.clear_pattern(pattern)
