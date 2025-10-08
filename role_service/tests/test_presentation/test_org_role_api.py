import pytest
from rest_framework.test import APIClient
from domain.organization_role_model import OrganizationRole
from domain.permission_model import Permission
from infrastructure.cache.org_permission_cache_service import OrgPermissionCacheService


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def cache_service():
    service = OrgPermissionCacheService()
    service.cache.clear_pattern("org_perm:*")
    return service


@pytest.mark.django_db
class TestOrgRoleAPI:
    def test_assign_org_role(self, api_client, cache_service):
        response = api_client.post(
            '/api/role/organizations/org-123/assign/',
            {'user_id': 'user-456'},
            format='json'
        )
        assert response.status_code == 201
        assert response.data['role'] == 'OWNER'
    
    def test_assign_duplicate_role(self, api_client, cache_service):
        OrganizationRole.objects.create(
            organization_id='org-123',
            user_id='user-456',
            role='OWNER'
        )
        response = api_client.post(
            '/api/role/organizations/org-123/assign/',
            {'user_id': 'user-456'},
            format='json'
        )
        assert response.status_code == 400
    
    def test_revoke_org_role(self, api_client, cache_service):
        OrganizationRole.objects.create(
            organization_id='org-123',
            user_id='user-456',
            role='ADMIN'
        )
        response = api_client.delete(
            '/api/role/organizations/org-123/revoke/',
            {'user_id': 'user-456'},
            format='json'
        )
        assert response.status_code == 200
        assert response.data['message'] == 'Role revoked successfully'
    
    def test_transfer_ownership(self, api_client, cache_service):
        OrganizationRole.objects.create(
            organization_id='org-123',
            user_id='user-456',
            role='OWNER'
        )
        response = api_client.post(
            '/api/role/organizations/org-123/transfer-ownership/',
            {'current_owner_id': 'user-456', 'new_owner_id': 'user-789'},
            format='json'
        )
        assert response.status_code == 200
        assert response.data['user_id'] == 'user-789'
        assert response.data['role'] == 'OWNER'
    
    def test_check_org_permission(self, api_client, cache_service):
        OrganizationRole.objects.create(
            organization_id='org-123',
            user_id='user-456',
            role='ADMIN'
        )
        Permission.objects.create(
            role='ADMIN',
            resource='EVENT',
            action='CREATE'
        )
        response = api_client.get(
            '/api/role/organizations/org-123/check/',
            {'user_id': 'user-456', 'resource': 'EVENT', 'action': 'CREATE'}
        )
        assert response.status_code == 200
        assert response.data['has_permission'] is True
        assert response.data['cached'] is False
    
    def test_check_org_permission_cached(self, api_client, cache_service):
        OrganizationRole.objects.create(
            organization_id='org-123',
            user_id='user-456',
            role='ADMIN'
        )
        Permission.objects.create(
            role='ADMIN',
            resource='EVENT',
            action='CREATE'
        )
        api_client.get(
            '/api/role/organizations/org-123/check/',
            {'user_id': 'user-456', 'resource': 'EVENT', 'action': 'CREATE'}
        )
        response = api_client.get(
            '/api/role/organizations/org-123/check/',
            {'user_id': 'user-456', 'resource': 'EVENT', 'action': 'CREATE'}
        )
        assert response.status_code == 200
        assert response.data['cached'] is True
