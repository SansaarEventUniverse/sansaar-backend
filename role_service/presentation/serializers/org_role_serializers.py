from rest_framework import serializers


class AssignOrgRoleSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=255)
    role = serializers.ChoiceField(choices=['OWNER', 'ADMIN', 'MEMBER'])


class RevokeOrgRoleSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=255)


class TransferOwnershipSerializer(serializers.Serializer):
    new_owner_id = serializers.CharField(max_length=255)


class CheckOrgPermissionSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=255)
    resource = serializers.CharField(max_length=50)
    action = serializers.CharField(max_length=50)


class OrgRoleResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    organization_id = serializers.CharField()
    user_id = serializers.CharField()
    role = serializers.CharField()
    is_active = serializers.BooleanField()
    assigned_at = serializers.DateTimeField()
