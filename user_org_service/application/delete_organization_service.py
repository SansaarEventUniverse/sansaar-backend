from domain.models import Organization


class DeleteOrganizationService:
    def delete_organization(self, org_id: str) -> dict:
        try:
            org = Organization.objects.get(org_id=org_id)
            org.delete()
            return {"message": f"Organization {org_id} deleted successfully"}
        except Organization.DoesNotExist:
            raise ValueError(f"Organization not found: {org_id}")
