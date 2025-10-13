import requests
from django.conf import settings


class OrgManagementService:
    def __init__(self):
        self.user_org_service_url = settings.USER_ORG_SERVICE_URL

    def get_organizations(self, page: int = 1, limit: int = 50) -> dict:
        url = f"{self.user_org_service_url}/api/user-org/organizations/"
        response = requests.get(url, params={"page": page, "limit": limit}, timeout=5)

        if response.status_code == 200:
            return response.json()
        raise Exception(f"Failed to fetch organizations: {response.text}")

    def get_organization_by_id(self, org_id: str) -> dict:
        url = f"{self.user_org_service_url}/api/user-org/organization/{org_id}/"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            raise ValueError(f"Organization not found: {org_id}")
        raise Exception(f"Failed to fetch organization: {response.text}")

    def delete_organization(self, org_id: str) -> dict:
        url = f"{self.user_org_service_url}/api/user-org/organization/{org_id}/delete/"
        response = requests.delete(url, timeout=5)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            raise ValueError(f"Organization not found: {org_id}")
        raise Exception(f"Failed to delete organization: {response.text}")
