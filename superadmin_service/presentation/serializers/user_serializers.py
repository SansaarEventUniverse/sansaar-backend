from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    id = serializers.CharField()
    email = serializers.EmailField()
    is_active = serializers.BooleanField()
    created_at = serializers.DateTimeField()


class UserListResponseSerializer(serializers.Serializer):
    users = UserSerializer(many=True)
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    limit = serializers.IntegerField()


class DeactivateUserResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    is_active = serializers.BooleanField()
    message = serializers.CharField()
