from django.core.exceptions import ValidationError
from domain.organization_role_model import OrganizationRole


class RevokeOrgRoleService:
    def revoke(self, organization_id, user_id):
        role = OrganizationRole.objects.filter(
            organization_id=organization_id,
            user_id=user_id,
            is_active=True
        ).first()
        
        if not role:
            raise ValidationError('No active role found for this user')
        
        if role.role == 'OWNER':
            raise ValidationError('Cannot revoke owner role. Transfer ownership first')
        
        role.revoke()
        return role
