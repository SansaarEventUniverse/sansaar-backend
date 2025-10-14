from rest_framework import serializers


class AssignEventRoleSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=255)
    role = serializers.ChoiceField(choices=['ADMIN', 'MEMBER', 'VOLUNTEER', 'ATTENDEE'])


class RevokeEventRoleSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=255)


class CheckEventPermissionSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=255)
    resource = serializers.CharField(max_length=50)
    action = serializers.CharField(max_length=50)


class EventRoleResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    event_id = serializers.CharField()
    user_id = serializers.CharField()
    role = serializers.CharField()
    is_active = serializers.BooleanField()
    assigned_at = serializers.DateTimeField()
