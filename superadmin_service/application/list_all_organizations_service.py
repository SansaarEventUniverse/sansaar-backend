class ListAllOrganizationsService:
    def __init__(self, org_management_service):
        self.org_management_service = org_management_service

    def list_organizations(self, page: int = 1, limit: int = 50) -> dict:
        return self.org_management_service.get_organizations(page, limit)
