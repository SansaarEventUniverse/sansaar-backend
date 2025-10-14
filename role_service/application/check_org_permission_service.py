from domain.organization_role_model import OrganizationRole
from domain.permission_model import Permission


class CheckOrgPermissionService:
    def check(self, organization_id, user_id, resource, action):
        role = OrganizationRole.objects.filter(
            organization_id=organization_id,
            user_id=user_id,
            is_active=True
        ).first()
        
        if not role:
            return False
        
        permission = Permission.objects.filter(
            role=role.role,
            resource=resource,
            action=action
        ).exists()
        
        return permission
