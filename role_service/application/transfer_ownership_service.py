from django.core.exceptions import ValidationError
from domain.organization_role_model import OrganizationRole


class TransferOwnershipService:
    def transfer(self, organization_id, current_owner_id, new_owner_id):
        current_owner = OrganizationRole.objects.filter(
            organization_id=organization_id,
            user_id=current_owner_id,
            role='OWNER',
            is_active=True
        ).first()
        
        if not current_owner:
            raise ValidationError('Current user is not the owner')
        
        current_owner.validate_ownership_transfer(new_owner_id)
        
        new_owner_role = OrganizationRole.objects.filter(
            organization_id=organization_id,
            user_id=new_owner_id,
            is_active=True
        ).first()
        
        if new_owner_role:
            new_owner_role.revoke()
        
        current_owner.revoke()
        
        return OrganizationRole.objects.create(
            organization_id=organization_id,
            user_id=new_owner_id,
            role='OWNER'
        )
