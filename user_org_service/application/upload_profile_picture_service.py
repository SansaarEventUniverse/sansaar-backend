from django.core.exceptions import ValidationError

from domain.user_profile_model import UserProfile
from infrastructure.storage.s3_service import S3Service


class UploadProfilePictureService:
    def __init__(self):
        self.s3_service = S3Service()

    def upload(self, user_id, file):
        # Validate file size (max 5MB)
        max_size = 5 * 1024 * 1024
        if file.size > max_size:
            raise ValidationError('File size must not exceed 5MB')

        try:
            profile = UserProfile.objects.get(user_id=user_id)
        except UserProfile.DoesNotExist:
            raise ValidationError('Profile not found')

        # Upload to S3
        url = self.s3_service.upload_profile_picture(file, user_id)
        profile.update_profile_picture(url)

        return profile
