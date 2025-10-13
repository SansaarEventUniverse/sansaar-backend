from rest_framework import serializers

from domain.user_profile_model import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "user_id",
            "email",
            "first_name",
            "last_name",
            "bio",
            "profile_picture_url",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["user_id", "email", "created_at", "updated_at"]


class UpdateProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    bio = serializers.CharField(max_length=500, required=False, allow_blank=True)


class UploadProfilePictureSerializer(serializers.Serializer):
    file = serializers.FileField()
