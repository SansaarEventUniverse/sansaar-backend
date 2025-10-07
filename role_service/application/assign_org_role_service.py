from django.core.exceptions import ValidationError
from domain.organization_role_model import OrganizationRole


class AssignOrgRoleService:
    def assign(self, organization_id, user_id, role):
        existing = OrganizationRole.objects.filter(
            organization_id=organization_id,
            user_id=user_id,
            is_active=True
        ).first()
        
        if existing:
            raise ValidationError('User already has an active role in this organization')
        
        if role == 'OWNER':
            existing_owner = OrganizationRole.get_active_owner(organization_id)
            if existing_owner:
                raise ValidationError('Organization already has an owner')
        
        return OrganizationRole.objects.create(
            organization_id=organization_id,
            user_id=user_id,
            role=role
        )
