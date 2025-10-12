from rest_framework import serializers


class SuperAdminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    mfa_token = serializers.CharField(max_length=6, min_length=6)


class SuperAdminLoginResponseSerializer(serializers.Serializer):
    token = serializers.CharField()
    admin_id = serializers.CharField()
    email = serializers.EmailField()


class SuperAdminLogoutSerializer(serializers.Serializer):
    message = serializers.CharField()
