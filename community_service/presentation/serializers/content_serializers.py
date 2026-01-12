from rest_framework import serializers
from domain.models import SharedContent, ContentCollaboration

class SharedContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedContent
        fields = ['id', 'title', 'description', 'content_type', 'content_url', 'creator_user_id', 'status', 'is_collaborative', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class ContentCollaborationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentCollaboration
        fields = ['id', 'content', 'user_id', 'role', 'joined_at']
        read_only_fields = ['id', 'joined_at']
