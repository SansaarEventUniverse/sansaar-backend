from domain.models import UserProfile


class DeleteProfilePictureService:
    def __init__(self, s3_service=None):
        self.s3_service = s3_service

    def delete_picture(self, user_id: str) -> dict:
        try:
            profile = UserProfile.objects.get(user_id=user_id)
            old_url = profile.profile_picture_url

            # Delete from S3 if service provided and URL exists
            if self.s3_service and old_url:
                try:
                    # Extract key from URL
                    key = old_url.split("/")[-1]
                    self.s3_service.delete_file(key)
                except Exception:
                    pass  # Continue even if S3 deletion fails

            profile.delete_profile_picture()
            return {"message": "Profile picture deleted successfully", "deleted_data": old_url}
        except UserProfile.DoesNotExist:
            raise ValueError(f"Profile not found for user: {user_id}")
