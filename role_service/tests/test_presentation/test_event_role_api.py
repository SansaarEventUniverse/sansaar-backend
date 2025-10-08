import pytest
from rest_framework.test import APIClient

from domain.event_role_model import EventRole
from domain.permission_model import Permission
from infrastructure.cache.permission_cache_service import PermissionCacheService


@pytest.mark.django_db
class TestEventRoleAPI:
    def setup_method(self):
        self.client = APIClient()
        cache = PermissionCacheService()
        cache.clear_all()

    def test_assign_event_role(self):
        response = self.client.post('/api/role/events/event-123/assign/', {
            'user_id': 'user-456',
            'role': 'ADMIN'
        })

        assert response.status_code == 201
        assert response.json()['event_id'] == 'event-123'
        assert response.json()['user_id'] == 'user-456'
        assert response.json()['role'] == 'ADMIN'

    def test_assign_role_already_exists(self):
        EventRole.objects.create(
            event_id='event-123',
            user_id='user-456',
            role='ORGANIZER'
        )

        response = self.client.post('/api/role/events/event-123/assign/', {
            'user_id': 'user-456',
            'role': 'VOLUNTEER'
        })

        assert response.status_code == 400

    def test_revoke_event_role(self):
        EventRole.objects.create(
            event_id='event-123',
            user_id='user-456',
            role='ORGANIZER'
        )

        response = self.client.delete('/api/role/events/event-123/revoke/', {
            'user_id': 'user-456'
        })

        assert response.status_code == 200

    def test_revoke_role_not_found(self):
        response = self.client.delete('/api/role/events/event-123/revoke/', {
            'user_id': 'user-456'
        })

        assert response.status_code == 404

    def test_check_event_permission(self):
        Permission.objects.create(
            role='ORGANIZER',
            resource='EVENT',
            action='DELETE'
        )
        EventRole.objects.create(
            event_id='event-123',
            user_id='user-456',
            role='ORGANIZER'
        )

        response = self.client.get('/api/role/events/event-123/check/', {
            'user_id': 'user-456',
            'resource': 'EVENT',
            'action': 'DELETE'
        })

        assert response.status_code == 200
        assert response.json()['has_permission'] is True

    def test_check_permission_denied(self):
        Permission.objects.create(
            role='VOLUNTEER',
            resource='EVENT',
            action='READ'
        )
        EventRole.objects.create(
            event_id='event-123',
            user_id='user-456',
            role='VOLUNTEER'
        )

        response = self.client.get('/api/role/events/event-123/check/', {
            'user_id': 'user-456',
            'resource': 'EVENT',
            'action': 'DELETE'
        })

        assert response.status_code == 200
        assert response.json()['has_permission'] is False
