from rest_framework import serializers
from domain.models import ResourceLibrary, SharedResource

class ResourceLibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceLibrary
        fields = ['id', 'name', 'description', 'category', 'created_by', 'is_public', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class SharedResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedResource
        fields = ['id', 'library', 'title', 'description', 'file_url', 'file_type', 'file_size', 'tags', 'download_count', 'uploaded_by', 'created_at', 'updated_at']
        read_only_fields = ['id', 'download_count', 'created_at', 'updated_at']
