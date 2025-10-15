from domain.models import UserProfile


class DeletePhoneService:
    def delete_phone(self, user_id: str) -> dict:
        try:
            profile = UserProfile.objects.get(user_id=user_id)
            old_phone = profile.phone
            profile.delete_phone()
            return {"message": "Phone deleted successfully", "deleted_data": old_phone}
        except UserProfile.DoesNotExist:
            raise ValueError(f"Profile not found for user: {user_id}")
