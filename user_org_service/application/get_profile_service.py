from django.core.exceptions import ValidationError

from domain.user_profile_model import UserProfile


class GetProfileService:
    def get_profile(self, user_id):
        try:
            return UserProfile.objects.get(user_id=user_id)
        except UserProfile.DoesNotExist:
            raise ValidationError('Profile not found')
