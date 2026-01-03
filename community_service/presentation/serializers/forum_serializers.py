from rest_framework import serializers
from domain.models import Forum, ForumPost

class ForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum
        fields = ['id', 'title', 'description', 'category', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class ForumPostSerializer(serializers.ModelSerializer):
    forum_title = serializers.CharField(source='forum.title', read_only=True)
    
    class Meta:
        model = ForumPost
        fields = ['id', 'forum', 'forum_title', 'author_name', 'author_email', 
                  'title', 'content', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
