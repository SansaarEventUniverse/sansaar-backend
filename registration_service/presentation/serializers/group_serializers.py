from rest_framework import serializers

from domain.group_registration import GroupRegistration, GroupMember


class GroupMemberSerializer(serializers.ModelSerializer):
    """Serializer for GroupMember."""
    
    class Meta:
        model = GroupMember
        fields = ['id', 'user_id', 'name', 'email', 'joined_at']


class GroupRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for GroupRegistration."""
    
    members = GroupMemberSerializer(many=True, read_only=True)
    
    class Meta:
        model = GroupRegistration
        fields = [
            'id', 'event_id', 'group_name', 'group_leader_id', 'group_leader_email',
            'min_size', 'max_size', 'current_size', 'status',
            'price_per_person', 'total_amount', 'members',
            'created_at', 'cancelled_at'
        ]


class CreateGroupSerializer(serializers.Serializer):
    """Serializer for creating groups."""
    
    group_name = serializers.CharField(max_length=255)
    group_leader_id = serializers.UUIDField()
    group_leader_email = serializers.EmailField()
    max_size = serializers.IntegerField(min_value=2)
    min_size = serializers.IntegerField(min_value=2, required=False)
    price_per_person = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)


class JoinGroupSerializer(serializers.Serializer):
    """Serializer for joining groups."""
    
    user_id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
