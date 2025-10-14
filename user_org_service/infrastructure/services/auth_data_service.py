import requests
from django.conf import settings


class AuthDataService:
    def __init__(self):
        self.auth_service_url = getattr(settings, "AUTH_SERVICE_URL", "http://localhost:8001")

    def get_auth_data(self, user_id: str) -> dict:
        url = f"{self.auth_service_url}/api/auth/user/{user_id}/"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception:
            return None
