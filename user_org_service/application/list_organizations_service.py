from domain.models import Organization


class ListOrganizationsService:
    def list_organizations(self, page: int = 1, limit: int = 50) -> dict:
        offset = (page - 1) * limit
        organizations = Organization.objects.all()[offset : offset + limit]
        total = Organization.objects.count()

        return {
            "organizations": list(
                organizations.values(
                    "org_id", "name", "description", "owner_user_id", "is_active", "created_at", "updated_at"
                )
            ),
            "total": total,
            "page": page,
            "limit": limit,
        }
