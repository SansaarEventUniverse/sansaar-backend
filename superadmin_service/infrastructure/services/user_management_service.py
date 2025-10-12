import requests
from django.conf import settings
from django.core.exceptions import ValidationError


class UserManagementService:
    def __init__(self):
        self.auth_service_url = getattr(settings, "AUTH_SERVICE_URL", "http://localhost:8001")
        self.user_org_service_url = getattr(settings, "USER_ORG_SERVICE_URL", "http://localhost:8002")

    def get_users(self, page: int = 1, limit: int = 50) -> dict:
        # Get users from user_org_service profiles endpoint
        try:
            response = requests.get(
                f"{self.user_org_service_url}/api/user-org/profiles/", params={"page": page, "limit": limit}, timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return {"users": [], "total": 0, "page": page, "limit": limit}

    def get_user_by_id(self, user_id: str) -> dict:
        # Try to get user profile from user_org_service
        try:
            response = requests.get(f"{self.user_org_service_url}/api/user-org/profile/{user_id}/", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            # Fallback to auth_service (not implemented yet)
            raise ValidationError(f"User not found: {user_id}")

    def deactivate_user(self, user_id: str) -> dict:
        # TODO: This endpoint needs to be implemented in auth_service
        try:
            response = requests.post(f"{self.auth_service_url}/api/auth/users/{user_id}/deactivate/", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise ValidationError(f"Failed to deactivate user: User deactivation not implemented in auth_service yet")
