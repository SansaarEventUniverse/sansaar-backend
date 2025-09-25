from django.core.exceptions import ValidationError

from domain.user_profile_model import UserProfile


class UpdateProfileService:
    def update_profile(self, user_id, first_name=None, last_name=None, bio=None):
        try:
            profile = UserProfile.objects.get(user_id=user_id)
        except UserProfile.DoesNotExist:
            raise ValidationError("Profile not found")

        profile.update_info(first_name=first_name, last_name=last_name, bio=bio)
        return profile
