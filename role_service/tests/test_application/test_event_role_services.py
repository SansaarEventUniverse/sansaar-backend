import pytest
from django.core.exceptions import ValidationError

from application.assign_event_role_service import AssignEventRoleService
from application.revoke_event_role_service import RevokeEventRoleService
from application.check_event_permission_service import CheckEventPermissionService
from domain.event_role_model import EventRole
from domain.permission_model import Permission


@pytest.mark.django_db
class TestAssignEventRoleService:
    def test_assign_role_success(self):
        service = AssignEventRoleService()
        role = service.execute(
            event_id='event-123',
            user_id='user-456',
            role='ORGANIZER'
        )
        
        assert role.event_id == 'event-123'
        assert role.user_id == 'user-456'
        assert role.role == 'ORGANIZER'
        assert role.is_active is True

    def test_assign_role_already_exists(self):
        EventRole.objects.create(
            event_id='event-123',
            user_id='user-456',
            role='ORGANIZER'
        )
        
        service = AssignEventRoleService()
        with pytest.raises(ValidationError):
            service.execute(
                event_id='event-123',
                user_id='user-456',
                role='VOLUNTEER'
            )


@pytest.mark.django_db
class TestRevokeEventRoleService:
    def test_revoke_role_success(self):
        role = EventRole.objects.create(
            event_id='event-123',
            user_id='user-456',
            role='ORGANIZER'
        )
        
        service = RevokeEventRoleService()
        result = service.execute(
            event_id='event-123',
            user_id='user-456'
        )
        
        assert result is True
        role.refresh_from_db()
        assert role.is_active is False

    def test_revoke_role_not_found(self):
        service = RevokeEventRoleService()
        result = service.execute(
            event_id='event-123',
            user_id='user-456'
        )
        
        assert result is False


@pytest.mark.django_db
class TestCheckEventPermissionService:
    def setup_method(self):
        Permission.objects.create(
            role='ORGANIZER',
            resource='EVENT',
            action='DELETE'
        )
        Permission.objects.create(
            role='VOLUNTEER',
            resource='EVENT',
            action='READ'
        )

    def test_check_permission_granted(self):
        EventRole.objects.create(
            event_id='event-123',
            user_id='user-456',
            role='ORGANIZER'
        )
        
        service = CheckEventPermissionService()
        result = service.execute(
            event_id='event-123',
            user_id='user-456',
            resource='EVENT',
            action='DELETE'
        )
        
        assert result is True

    def test_check_permission_denied(self):
        EventRole.objects.create(
            event_id='event-123',
            user_id='user-456',
            role='VOLUNTEER'
        )
        
        service = CheckEventPermissionService()
        result = service.execute(
            event_id='event-123',
            user_id='user-456',
            resource='EVENT',
            action='DELETE'
        )
        
        assert result is False

    def test_check_permission_no_role(self):
        service = CheckEventPermissionService()
        result = service.execute(
            event_id='event-123',
            user_id='user-456',
            resource='EVENT',
            action='DELETE'
        )
        
        assert result is False
