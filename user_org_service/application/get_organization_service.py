from domain.models import Organization


class GetOrganizationService:
    def get_organization(self, org_id: str) -> dict:
        try:
            org = Organization.objects.get(org_id=org_id)
            return {
                "org_id": org.org_id,
                "name": org.name,
                "description": org.description,
                "owner_user_id": org.owner_user_id,
                "is_active": org.is_active,
                "created_at": org.created_at,
                "updated_at": org.updated_at,
            }
        except Organization.DoesNotExist:
            raise ValueError(f"Organization not found: {org_id}")
