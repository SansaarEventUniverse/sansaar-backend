from rest_framework import serializers


class OrganizationSerializer(serializers.Serializer):
    org_id = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField(allow_null=True)
    owner_user_id = serializers.CharField()
    is_active = serializers.BooleanField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
