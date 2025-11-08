from typing import Dict, Any
import uuid
from django.core.exceptions import ValidationError

from domain.media import MediaGallery, MediaItem


class MediaManagementService:
    """Service for managing media galleries."""
    
    def get_or_create_gallery(self, event_id: uuid.UUID) -> MediaGallery:
        """Get or create gallery for event."""
        gallery, created = MediaGallery.objects.get_or_create(event_id=event_id)
        return gallery
    
    def add_media_item(self, event_id: uuid.UUID, data: Dict[str, Any]) -> MediaItem:
        """Add media item to gallery."""
        gallery = self.get_or_create_gallery(event_id)
        
        item = MediaItem(
            gallery=gallery,
            file_name=data['file_name'],
            file_type=data['file_type'],
            file_size=data['file_size'],
            mime_type=data['mime_type'],
            s3_key=data['s3_key'],
            cdn_url=data.get('cdn_url', ''),
            width=data.get('width'),
            height=data.get('height'),
        )
        item.clean()
        item.save()
        
        # Update gallery stats
        gallery.add_item(item.file_size)
        
        return item
    
    def delete_media_item(self, item_id: uuid.UUID) -> None:
        """Delete media item."""
        try:
            item = MediaItem.objects.get(id=item_id)
            gallery = item.gallery
            file_size = item.file_size
            
            item.delete()
            gallery.remove_item(file_size)
        except MediaItem.DoesNotExist:
            raise ValidationError('Media item not found')


class MediaUploadService:
    """Service for media upload validation."""
    
    ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
    ALLOWED_VIDEO_TYPES = ['video/mp4', 'video/webm']
    ALLOWED_DOCUMENT_TYPES = ['application/pdf']
    
    def validate_upload(self, file_type: str, mime_type: str, file_size: int) -> bool:
        """Validate media upload."""
        # Check file size (50MB max)
        max_size = 50 * 1024 * 1024
        if file_size > max_size:
            raise ValidationError('File size exceeds 50MB limit')
        
        # Check mime type
        allowed_types = []
        if file_type == 'image':
            allowed_types = self.ALLOWED_IMAGE_TYPES
        elif file_type == 'video':
            allowed_types = self.ALLOWED_VIDEO_TYPES
        elif file_type == 'document':
            allowed_types = self.ALLOWED_DOCUMENT_TYPES
        
        if mime_type not in allowed_types:
            raise ValidationError(f'File type {mime_type} not allowed')
        
        return True
