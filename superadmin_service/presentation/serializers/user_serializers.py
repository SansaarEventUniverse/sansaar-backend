from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    bio = serializers.CharField(required=False, allow_blank=True)
    profile_picture_url = serializers.URLField(required=False, allow_null=True)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class UserListResponseSerializer(serializers.Serializer):
    users = UserSerializer(many=True)
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    limit = serializers.IntegerField()


class DeactivateUserResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    is_active = serializers.BooleanField()
    message = serializers.CharField()
