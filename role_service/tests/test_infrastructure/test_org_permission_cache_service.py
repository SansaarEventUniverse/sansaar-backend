import pytest
from infrastructure.cache.org_permission_cache_service import OrgPermissionCacheService


@pytest.mark.django_db
class TestOrgPermissionCacheService:
    def setup_method(self):
        self.service = OrgPermissionCacheService()
        self.service.cache.clear_pattern("org_perm:*")
    
    def test_cache_and_get_permission(self):
        self.service.cache_permission('org-123', 'user-456', True)
        result = self.service.get_cached_permission('org-123', 'user-456')
        assert result is True
    
    def test_get_nonexistent_permission(self):
        result = self.service.get_cached_permission('org-999', 'user-999')
        assert result is None
    
    def test_invalidate_user_cache(self):
        self.service.cache_permission('org-123', 'user-456', True)
        self.service.invalidate_user_cache('org-123', 'user-456')
        result = self.service.get_cached_permission('org-123', 'user-456')
        assert result is None
    
    def test_invalidate_org_cache(self):
        self.service.cache_permission('org-123', 'user-456', True)
        self.service.cache_permission('org-123', 'user-789', False)
        self.service.invalidate_org_cache('org-123')
        result1 = self.service.get_cached_permission('org-123', 'user-456')
        result2 = self.service.get_cached_permission('org-123', 'user-789')
        assert result1 is None
        assert result2 is None
