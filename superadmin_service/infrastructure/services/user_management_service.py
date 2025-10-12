import requests
from django.conf import settings
from django.core.exceptions import ValidationError


class UserManagementService:
    def __init__(self):
        self.auth_service_url = getattr(settings, "AUTH_SERVICE_URL", "http://localhost:8001")

    def get_users(self, page: int = 1, limit: int = 50) -> dict:
        try:
            response = requests.get(
                f"{self.auth_service_url}/api/auth/users/", params={"page": page, "limit": limit}, timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise ValidationError(f"Failed to fetch users: {str(e)}")

    def get_user_by_id(self, user_id: str) -> dict:
        try:
            response = requests.get(f"{self.auth_service_url}/api/auth/users/{user_id}/", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise ValidationError(f"Failed to fetch user: {str(e)}")

    def deactivate_user(self, user_id: str) -> dict:
        try:
            response = requests.post(f"{self.auth_service_url}/api/auth/users/{user_id}/deactivate/", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise ValidationError(f"Failed to deactivate user: {str(e)}")
