from rest_framework import serializers

from domain.document import Document


class DocumentSerializer(serializers.ModelSerializer):
    """Serializer for Document."""
    
    class Meta:
        model = Document
        fields = [
            'id', 'event_id', 'title', 'description', 'document_type',
            'file_name', 'file_size', 'mime_type', 'access_level',
            'is_required', 'version', 'download_count', 'created_at'
        ]


class UploadDocumentSerializer(serializers.Serializer):
    """Serializer for document upload request."""
    
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)
    document_type = serializers.ChoiceField(choices=Document.DOCUMENT_TYPES)
    file_name = serializers.CharField(max_length=255)
    file_size = serializers.IntegerField()
    mime_type = serializers.CharField(max_length=100)
    access_level = serializers.ChoiceField(choices=Document.ACCESS_LEVELS, default='public')
    is_required = serializers.BooleanField(default=False)
    created_by = serializers.UUIDField()
