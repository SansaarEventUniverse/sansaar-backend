from rest_framework import serializers

from domain.media import MediaGallery, MediaItem


class MediaItemSerializer(serializers.ModelSerializer):
    """Serializer for MediaItem."""
    
    class Meta:
        model = MediaItem
        fields = [
            'id', 'file_name', 'file_type', 'file_size', 'mime_type',
            'cdn_url', 'width', 'height', 'duration_seconds',
            'is_processed', 'is_primary', 'created_at'
        ]


class MediaGallerySerializer(serializers.ModelSerializer):
    """Serializer for MediaGallery."""
    
    items = MediaItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = MediaGallery
        fields = ['id', 'event_id', 'total_items', 'total_size_bytes', 'items']


class UploadMediaSerializer(serializers.Serializer):
    """Serializer for media upload request."""
    
    file_name = serializers.CharField(max_length=255)
    file_type = serializers.ChoiceField(choices=['image', 'video', 'document'])
    file_size = serializers.IntegerField()
    mime_type = serializers.CharField(max_length=100)
