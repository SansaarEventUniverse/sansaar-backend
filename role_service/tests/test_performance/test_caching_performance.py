import pytest
import time
from infrastructure.cache.permission_cache_service import PermissionCacheService
from infrastructure.cache.org_permission_cache_service import OrgPermissionCacheService


class TestCachingPerformance:
    def setup_method(self):
        self.event_cache = PermissionCacheService()
        self.org_cache = OrgPermissionCacheService()
        self.event_cache.clear_all()
        self.org_cache.cache.clear_pattern("org_perm:*")
    
    def test_event_cache_performance(self):
        start = time.time()
        for i in range(100):
            self.event_cache.cache_permission(f'event-{i}', f'user-{i}', True)
        cache_time = time.time() - start
        
        start = time.time()
        for i in range(100):
            result = self.event_cache.get_cached_permission(f'event-{i}', f'user-{i}')
            assert result is True
        retrieve_time = time.time() - start
        
        assert cache_time < 1.0
        assert retrieve_time < 0.5
    
    def test_org_cache_performance(self):
        start = time.time()
        for i in range(100):
            self.org_cache.cache_permission(f'org-{i}', f'user-{i}', True)
        cache_time = time.time() - start
        
        start = time.time()
        for i in range(100):
            result = self.org_cache.get_cached_permission(f'org-{i}', f'user-{i}')
            assert result is True
        retrieve_time = time.time() - start
        
        assert cache_time < 1.0
        assert retrieve_time < 0.5
    
    def test_cache_invalidation_performance(self):
        for i in range(50):
            self.event_cache.cache_permission('event-test', f'user-{i}', True)
        
        start = time.time()
        self.event_cache.invalidate_event_cache('event-test')
        invalidate_time = time.time() - start
        
        assert invalidate_time < 0.5
        
        for i in range(50):
            result = self.event_cache.get_cached_permission('event-test', f'user-{i}')
            assert result is None
    
    def test_bulk_permission_check(self):
        for i in range(100):
            self.event_cache.cache_permission('event-bulk', f'user-{i}', i % 2 == 0)
        
        start = time.time()
        results = []
        for i in range(100):
            result = self.event_cache.get_cached_permission('event-bulk', f'user-{i}')
            results.append(result)
        bulk_time = time.time() - start
        
        assert bulk_time < 0.5
        assert len([r for r in results if r is True]) == 50
        assert len([r for r in results if r is False]) == 50
