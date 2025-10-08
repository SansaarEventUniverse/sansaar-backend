import pytest
from django.core.exceptions import ValidationError
from domain.organization_role_model import OrganizationRole


@pytest.mark.django_db
class TestOrganizationRoleModel:
    def test_create_organization_role(self):
        role = OrganizationRole.objects.create(
            organization_id='org-123',
            user_id='user-456',
            role='OWNER'
        )
        assert role.organization_id == 'org-123'
        assert role.user_id == 'user-456'
        assert role.role == 'OWNER'
        assert role.is_active is True
        assert role.revoked_at is None
    
    def test_revoke_role(self):
        role = OrganizationRole.objects.create(
            organization_id='org-123',
            user_id='user-456',
            role='ADMIN'
        )
        role.revoke()
        assert role.is_active is False
        assert role.revoked_at is not None
    
    def test_validate_ownership_transfer_success(self):
        role = OrganizationRole.objects.create(
            organization_id='org-123',
            user_id='user-456',
            role='OWNER'
        )
        role.validate_ownership_transfer('user-789')
    
    def test_validate_ownership_transfer_not_owner(self):
        role = OrganizationRole.objects.create(
            organization_id='org-123',
            user_id='user-456',
            role='OWNER'
        )
        role.validate_ownership_transfer('user-789')
    
    def test_validate_ownership_transfer_inactive(self):
        role = OrganizationRole.objects.create(
            organization_id='org-123',
            user_id='user-456',
            role='OWNER',
            is_active=False
        )
        with pytest.raises(ValidationError, match='Cannot transfer from inactive owner'):
            role.validate_ownership_transfer('user-789')
    
    def test_validate_ownership_transfer_to_self(self):
        role = OrganizationRole.objects.create(
            organization_id='org-123',
            user_id='user-456',
            role='OWNER'
        )
        with pytest.raises(ValidationError, match='Cannot transfer ownership to self'):
            role.validate_ownership_transfer('user-456')
    
    def test_get_active_owner(self):
        OrganizationRole.objects.create(
            organization_id='org-123',
            user_id='user-456',
            role='OWNER'
        )
        owner = OrganizationRole.get_active_owner('org-123')
        assert owner is not None
        assert owner.role == 'OWNER'
        assert owner.user_id == 'user-456'
    
    def test_get_active_owner_none(self):
        owner = OrganizationRole.get_active_owner('org-999')
        assert owner is None
