import pytest
from django.core.exceptions import ValidationError

from domain.event_role_model import EventRole
from domain.permission_model import Permission


@pytest.mark.django_db
class TestEventRoleModel:
    def test_create_event_role(self):
        role = EventRole.objects.create(
            event_id='event-123',
            user_id='user-456',
            role='ORGANIZER'
        )
        
        assert role.event_id == 'event-123'
        assert role.user_id == 'user-456'
        assert role.role == 'ORGANIZER'
        assert role.is_active is True

    def test_role_choices_validation(self):
        valid_roles = ['ORGANIZATION', 'ORGANIZER', 'VOLUNTEER', 'ATTENDEE']
        
        for role_type in valid_roles:
            role = EventRole(
                event_id='event-123',
                user_id='user-456',
                role=role_type
            )
            role.full_clean()

    def test_revoke_role(self):
        role = EventRole.objects.create(
            event_id='event-123',
            user_id='user-456',
            role='ORGANIZER'
        )
        
        role.revoke()
        
        assert role.is_active is False
        assert role.revoked_at is not None

    def test_unique_active_role_per_user_event(self):
        EventRole.objects.create(
            event_id='event-123',
            user_id='user-456',
            role='ORGANIZER'
        )
        
        with pytest.raises(Exception):
            EventRole.objects.create(
                event_id='event-123',
                user_id='user-456',
                role='MODERATOR'
            )


@pytest.mark.django_db
class TestPermissionModel:
    def test_create_permission(self):
        permission = Permission.objects.create(
            role='ORGANIZER',
            resource='EVENT',
            action='DELETE'
        )
        
        assert permission.role == 'ORGANIZER'
        assert permission.resource == 'EVENT'
        assert permission.action == 'DELETE'

    def test_permission_string_representation(self):
        permission = Permission.objects.create(
            role='ORGANIZER',
            resource='EVENT',
            action='UPDATE'
        )
        
        assert str(permission) == 'ORGANIZER:EVENT:UPDATE'
