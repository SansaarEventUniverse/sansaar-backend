from rest_framework import serializers
from domain.models import InterestGroup, GroupMembership

class InterestGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterestGroup
        fields = ['id', 'name', 'description', 'category', 'creator_user_id', 'is_active', 'max_members', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class GroupMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMembership
        fields = ['id', 'group', 'user_id', 'status', 'role', 'joined_at', 'updated_at']
        read_only_fields = ['id', 'joined_at', 'updated_at']
