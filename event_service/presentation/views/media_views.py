import uuid
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError

from application.media_service import MediaManagementService, MediaUploadService
from infrastructure.services.s3_media_service import S3MediaService
from domain.media import MediaGallery
from presentation.serializers.media_serializers import (
    MediaGallerySerializer,
    UploadMediaSerializer,
)


@api_view(['POST'])
def upload_media(request, event_id):
    """Generate presigned URL for media upload."""
    serializer = UploadMediaSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        event_uuid = uuid.UUID(event_id)
    except ValueError:
        return Response({'error': 'Invalid event ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Validate upload
    upload_service = MediaUploadService()
    try:
        upload_service.validate_upload(
            serializer.validated_data['file_type'],
            serializer.validated_data['mime_type'],
            serializer.validated_data['file_size']
        )
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    # Generate upload URL
    s3_service = S3MediaService()
    upload_data = s3_service.generate_upload_url(
        event_uuid,
        serializer.validated_data['file_name'],
        serializer.validated_data['mime_type']
    )
    
    # Create media item record
    media_service = MediaManagementService()
    item = media_service.add_media_item(event_uuid, {
        **serializer.validated_data,
        's3_key': upload_data['s3_key'],
        'cdn_url': upload_data['cdn_url'],
    })
    
    return Response({
        'upload_url': upload_data['upload_url'],
        'media_id': str(item.id),
        'cdn_url': upload_data['cdn_url'],
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_media_gallery(request, event_id):
    """Get media gallery for event."""
    try:
        event_uuid = uuid.UUID(event_id)
    except ValueError:
        return Response({'error': 'Invalid event ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        gallery = MediaGallery.objects.prefetch_related('items').get(event_id=event_uuid)
        return Response(MediaGallerySerializer(gallery).data)
    except MediaGallery.DoesNotExist:
        return Response({'items': [], 'total_items': 0}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_media(request, event_id, media_id):
    """Delete media item."""
    try:
        media_uuid = uuid.UUID(media_id)
    except ValueError:
        return Response({'error': 'Invalid media ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        service = MediaManagementService()
        service.delete_media_item(media_uuid)
        return Response(status=status.HTTP_204_NO_CONTENT)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
