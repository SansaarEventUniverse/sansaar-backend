from infrastructure.cache.cache_service import CacheService


class OrgPermissionCacheService:
    def __init__(self):
        self.cache = CacheService()
    
    def cache_permission(self, organization_id, user_id, has_permission):
        key = f"org_perm:{organization_id}:{user_id}"
        self.cache.set(key, str(has_permission))
    
    def get_cached_permission(self, organization_id, user_id):
        key = f"org_perm:{organization_id}:{user_id}"
        value = self.cache.get(key)
        if value is None:
            return None
        return value == 'True'
    
    def invalidate_user_cache(self, organization_id, user_id):
        key = f"org_perm:{organization_id}:{user_id}"
        self.cache.delete(key)
    
    def invalidate_org_cache(self, organization_id):
        pattern = f"org_perm:{organization_id}:*"
        self.cache.clear_pattern(pattern)
