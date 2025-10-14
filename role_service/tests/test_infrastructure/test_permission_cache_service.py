import pytest
import json

from infrastructure.cache.permission_cache_service import PermissionCacheService
from domain.event_role_model import EventRole
from domain.permission_model import Permission


@pytest.mark.django_db
class TestPermissionCacheService:
    def setup_method(self):
        self.cache_service = PermissionCacheService()
        self.cache_service.clear_all()

    def test_cache_permission(self):
        self.cache_service.cache_permission(
            event_id='event-123',
            user_id='user-456',
            has_permission=True
        )
        
        result = self.cache_service.get_cached_permission(
            event_id='event-123',
            user_id='user-456'
        )
        
        assert result is True

    def test_cache_miss(self):
        result = self.cache_service.get_cached_permission(
            event_id='event-123',
            user_id='user-456'
        )
        
        assert result is None

    def test_invalidate_user_cache(self):
        self.cache_service.cache_permission(
            event_id='event-123',
            user_id='user-456',
            has_permission=True
        )
        
        self.cache_service.invalidate_user_cache(
            event_id='event-123',
            user_id='user-456'
        )
        
        result = self.cache_service.get_cached_permission(
            event_id='event-123',
            user_id='user-456'
        )
        
        assert result is None

    def test_invalidate_event_cache(self):
        self.cache_service.cache_permission(
            event_id='event-123',
            user_id='user-456',
            has_permission=True
        )
        
        self.cache_service.invalidate_event_cache('event-123')
        
        result = self.cache_service.get_cached_permission(
            event_id='event-123',
            user_id='user-456'
        )
        
        assert result is None
