import pytest
from domain.event_role_model import EventRole
from domain.organization_role_model import OrganizationRole


@pytest.mark.django_db
class TestRoleEventContracts:
    def test_role_assigned_event_contract(self):
        role = EventRole.objects.create(
            event_id='event-123',
            user_id='user-456',
            role='ADMIN'
        )
        
        assert role.event_id == 'event-123'
        assert role.user_id == 'user-456'
        assert role.role == 'ADMIN'
        assert role.is_active is True
        assert role.assigned_at is not None
        assert role.revoked_at is None
    
    def test_role_revoked_event_contract(self):
        role = EventRole.objects.create(
            event_id='event-123',
            user_id='user-456',
            role='ADMIN'
        )
        
        role.revoke()
        
        assert role.is_active is False
        assert role.revoked_at is not None
    
    def test_ownership_transferred_event_contract(self):
        org_role = OrganizationRole.objects.create(
            organization_id='org-123',
            user_id='user-owner',
            role='OWNER'
        )
        
        org_role.validate_ownership_transfer('user-new-owner')
        
        org_role.user_id = 'user-new-owner'
        org_role.save()
        
        assert org_role.user_id == 'user-new-owner'
        assert org_role.role == 'OWNER'
        assert org_role.is_active is True
    
    def test_permission_check_event_contract(self):
        from domain.permission_model import Permission
        
        permission = Permission.objects.create(
            role='ADMIN',
            resource='EVENT',
            action='CREATE'
        )
        
        assert permission.role == 'ADMIN'
        assert permission.resource == 'EVENT'
        assert permission.action == 'CREATE'
        assert str(permission) == 'ADMIN:EVENT:CREATE'
    
    def test_multiple_roles_same_event_contract(self):
        EventRole.objects.create(
            event_id='event-multi',
            user_id='user-1',
            role='ADMIN'
        )
        EventRole.objects.create(
            event_id='event-multi',
            user_id='user-2',
            role='MEMBER'
        )
        
        roles = EventRole.objects.filter(event_id='event-multi', is_active=True)
        assert roles.count() == 2
        assert set(r.role for r in roles) == {'ADMIN', 'MEMBER'}
    
    def test_organization_owner_uniqueness_contract(self):
        OrganizationRole.objects.create(
            organization_id='org-unique',
            user_id='user-owner',
            role='OWNER'
        )
        
        owner = OrganizationRole.get_active_owner('org-unique')
        assert owner is not None
        assert owner.user_id == 'user-owner'
