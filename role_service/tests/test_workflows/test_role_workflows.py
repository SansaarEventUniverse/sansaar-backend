import pytest
from rest_framework.test import APIClient
from domain.organization_role_model import OrganizationRole
from domain.event_role_model import EventRole
from domain.permission_model import Permission
from infrastructure.cache.permission_cache_service import PermissionCacheService


@pytest.mark.django_db
class TestRoleWorkflows:
    def setup_method(self):
        self.client = APIClient()
        self.cache = PermissionCacheService()
        self.cache.clear_all()
        Permission.objects.create(role='ADMIN', resource='EVENT', action='CREATE')
        Permission.objects.create(role='ADMIN', resource='EVENT', action='DELETE')
        Permission.objects.create(role='MEMBER', resource='EVENT', action='READ')
    
    def test_complete_organization_workflow(self):
        response = self.client.post(
            '/api/role/organizations/org-workflow/assign/',
            {'user_id': 'user-owner'},
            format='json'
        )
        assert response.status_code == 201
        assert response.data['role'] == 'OWNER'
        
        response = self.client.post(
            '/api/role/organizations/org-workflow/transfer-ownership/',
            {'current_owner_id': 'user-owner', 'new_owner_id': 'user-new-owner'},
            format='json'
        )
        assert response.status_code == 200
        assert response.data['user_id'] == 'user-new-owner'
        
        owner = OrganizationRole.get_active_owner('org-workflow')
        assert owner.user_id == 'user-new-owner'
    
    def test_complete_event_role_workflow(self):
        response = self.client.post(
            '/api/role/events/event-workflow/assign/',
            {'user_id': 'user-admin', 'role': 'ADMIN'},
            format='json'
        )
        assert response.status_code == 201
        
        response = self.client.get(
            '/api/role/events/event-workflow/check/',
            {'user_id': 'user-admin', 'resource': 'EVENT', 'action': 'CREATE'}
        )
        assert response.status_code == 200
        assert response.data['has_permission'] is True
        assert response.data['cached'] is False
        
        response = self.client.get(
            '/api/role/events/event-workflow/check/',
            {'user_id': 'user-admin', 'resource': 'EVENT', 'action': 'CREATE'}
        )
        assert response.data['cached'] is True
        
        response = self.client.delete(
            '/api/role/events/event-workflow/revoke/',
            {'user_id': 'user-admin'},
            format='json'
        )
        assert response.status_code == 200
        
        response = self.client.get(
            '/api/role/events/event-workflow/check/',
            {'user_id': 'user-admin', 'resource': 'EVENT', 'action': 'CREATE'}
        )
        assert response.data['has_permission'] is False
    
    def test_multi_user_event_roles(self):
        self.client.post(
            '/api/role/events/event-multi/assign/',
            {'user_id': 'user-admin', 'role': 'ADMIN'},
            format='json'
        )
        self.client.post(
            '/api/role/events/event-multi/assign/',
            {'user_id': 'user-member', 'role': 'MEMBER'},
            format='json'
        )
        
        response = self.client.get(
            '/api/role/events/event-multi/check/',
            {'user_id': 'user-admin', 'resource': 'EVENT', 'action': 'DELETE'}
        )
        assert response.data['has_permission'] is True
        
        response = self.client.get(
            '/api/role/events/event-multi/check/',
            {'user_id': 'user-member', 'resource': 'EVENT', 'action': 'DELETE'}
        )
        assert response.data['has_permission'] is False
        
        response = self.client.get(
            '/api/role/events/event-multi/check/',
            {'user_id': 'user-admin', 'resource': 'EVENT', 'action': 'CREATE'}
        )
        assert response.data['has_permission'] is True
    
    def test_cache_invalidation_on_role_change(self):
        self.client.post(
            '/api/role/events/event-cache/assign/',
            {'user_id': 'user-test', 'role': 'ADMIN'},
            format='json'
        )
        
        self.client.get(
            '/api/role/events/event-cache/check/',
            {'user_id': 'user-test', 'resource': 'EVENT', 'action': 'CREATE'}
        )
        
        cached = self.cache.get_cached_permission('event-cache', 'user-test')
        assert cached is not None
        
        self.client.delete(
            '/api/role/events/event-cache/revoke/',
            {'user_id': 'user-test'},
            format='json'
        )
        
        cached = self.cache.get_cached_permission('event-cache', 'user-test')
        assert cached is None
