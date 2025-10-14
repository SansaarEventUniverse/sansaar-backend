from domain.models import UserProfile


class ExportUserDataService:
    def __init__(self, auth_data_service=None):
        self.auth_data_service = auth_data_service

    def export_data(self, user_id: str) -> dict:
        try:
            profile = UserProfile.objects.get(user_id=user_id)

            # Collect profile data
            export_data = {
                "user_id": profile.user_id,
                "email": profile.email,
                "first_name": profile.first_name,
                "last_name": profile.last_name,
                "bio": profile.bio,
                "phone": profile.phone,
                "address": profile.address,
                "profile_picture_url": profile.profile_picture_url,
                "created_at": profile.created_at.isoformat(),
                "updated_at": profile.updated_at.isoformat(),
            }

            # Add auth data if service available
            if self.auth_data_service:
                try:
                    auth_data = self.auth_data_service.get_auth_data(user_id)
                    export_data["auth_data"] = auth_data
                except Exception:
                    export_data["auth_data"] = None

            return export_data
        except UserProfile.DoesNotExist:
            raise ValueError(f"Profile not found for user: {user_id}")
