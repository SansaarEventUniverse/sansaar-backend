from domain.models import UserProfile


class DeleteAddressService:
    def delete_address(self, user_id: str) -> dict:
        try:
            profile = UserProfile.objects.get(user_id=user_id)
            old_address = profile.address
            profile.delete_address()
            return {"message": "Address deleted successfully", "deleted_data": old_address}
        except UserProfile.DoesNotExist:
            raise ValueError(f"Profile not found for user: {user_id}")
