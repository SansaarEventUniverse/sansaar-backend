import pytest
from django.core.exceptions import ValidationError
from application.assign_org_role_service import AssignOrgRoleService
from application.revoke_org_role_service import RevokeOrgRoleService
from application.transfer_ownership_service import TransferOwnershipService
from application.check_org_permission_service import CheckOrgPermissionService
from domain.organization_role_model import OrganizationRole
from domain.permission_model import Permission


@pytest.mark.django_db
class TestAssignOrgRoleService:
    def test_assign_role(self):
        service = AssignOrgRoleService()
        role = service.assign('org-123', 'user-456')
        assert role.organization_id == 'org-123'
        assert role.user_id == 'user-456'
        assert role.role == 'OWNER'
    
    def test_assign_duplicate_role(self):
        OrganizationRole.objects.create(
            organization_id='org-123',
            user_id='user-456',
            role='OWNER'
        )
        service = AssignOrgRoleService()
        with pytest.raises(ValidationError, match='User already has an active role'):
            service.assign('org-123', 'user-456')
    
    def test_assign_owner_when_exists(self):
        OrganizationRole.objects.create(
            organization_id='org-123',
            user_id='user-456',
            role='OWNER'
        )
        service = AssignOrgRoleService()
        with pytest.raises(ValidationError, match='Organization already has an owner'):
            service.assign('org-123', 'user-789')


@pytest.mark.django_db
class TestRevokeOrgRoleService:
    def test_revoke_role(self):
        OrganizationRole.objects.create(
            organization_id='org-123',
            user_id='user-456',
            role='ADMIN'
        )
        service = RevokeOrgRoleService()
        role = service.revoke('org-123', 'user-456')
        assert role.is_active is False
    
    def test_revoke_nonexistent_role(self):
        service = RevokeOrgRoleService()
        with pytest.raises(ValidationError, match='No active role found'):
            service.revoke('org-123', 'user-999')
    
    def test_revoke_owner_role(self):
        OrganizationRole.objects.create(
            organization_id='org-123',
            user_id='user-456',
            role='OWNER'
        )
        service = RevokeOrgRoleService()
        with pytest.raises(ValidationError, match='Cannot revoke owner role'):
            service.revoke('org-123', 'user-456')


@pytest.mark.django_db
class TestTransferOwnershipService:
    def test_transfer_ownership(self):
        OrganizationRole.objects.create(
            organization_id='org-123',
            user_id='user-456',
            role='OWNER'
        )
        service = TransferOwnershipService()
        new_owner = service.transfer('org-123', 'user-456', 'user-789')
        assert new_owner.user_id == 'user-789'
        assert new_owner.role == 'OWNER'
        assert new_owner.is_active is True
    
    def test_transfer_ownership_not_owner(self):
        OrganizationRole.objects.create(
            organization_id='org-123',
            user_id='user-456',
            role='OWNER'
        )
        service = TransferOwnershipService()
        with pytest.raises(ValidationError, match='Current user is not the owner'):
            service.transfer('org-123', 'user-999', 'user-789')


@pytest.mark.django_db
class TestCheckOrgPermissionService:
    def test_check_permission_granted(self):
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
        service = CheckOrgPermissionService()
        has_permission = service.check('org-123', 'user-456', 'EVENT', 'CREATE')
        assert has_permission is True
    
    def test_check_permission_denied(self):
        OrganizationRole.objects.create(
            organization_id='org-123',
            user_id='user-456',
            role='MEMBER'
        )
        service = CheckOrgPermissionService()
        has_permission = service.check('org-123', 'user-456', 'EVENT', 'DELETE')
        assert has_permission is False
    
    def test_check_permission_no_role(self):
        service = CheckOrgPermissionService()
        has_permission = service.check('org-123', 'user-999', 'EVENT', 'CREATE')
        assert has_permission is False
