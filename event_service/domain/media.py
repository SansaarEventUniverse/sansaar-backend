import uuid
from django.db import models
from django.core.exceptions import ValidationError


class MediaGallery(models.Model):
    """Media gallery model for event media."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_id = models.UUIDField(unique=True)
    
    # Metadata
    total_items = models.IntegerField(default=0)
    total_size_bytes = models.BigIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'media_galleries'
        indexes = [
            models.Index(fields=['event_id']),
        ]
    
    def add_item(self, size_bytes: int) -> None:
        """Add item to gallery."""
        self.total_items += 1
        self.total_size_bytes += size_bytes
        self.save()
    
    def remove_item(self, size_bytes: int) -> None:
        """Remove item from gallery."""
        self.total_items = max(0, self.total_items - 1)
        self.total_size_bytes = max(0, self.total_size_bytes - size_bytes)
        self.save()
    
    def __str__(self):
        return f"Gallery for event {self.event_id} ({self.total_items} items)"


class MediaItem(models.Model):
    """Media item model for photos, videos, documents."""
    
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('document', 'Document'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    gallery = models.ForeignKey(MediaGallery, on_delete=models.CASCADE, related_name='items')
    
    # File details
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=20, choices=MEDIA_TYPES)
    file_size = models.BigIntegerField()  # in bytes
    mime_type = models.CharField(max_length=100)
    
    # Storage
    s3_key = models.CharField(max_length=500)
    cdn_url = models.URLField(max_length=500, blank=True)
    
    # Metadata
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    duration_seconds = models.IntegerField(null=True, blank=True)
    
    # Status
    is_processed = models.BooleanField(default=False)
    is_primary = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'media_items'
        indexes = [
            models.Index(fields=['gallery', '-created_at']),
            models.Index(fields=['file_type']),
        ]
        ordering = ['-created_at']
    
    def clean(self):
        """Validate media item."""
        # Max file size: 50MB
        max_size = 50 * 1024 * 1024
        if self.file_size > max_size:
            raise ValidationError(f'File size exceeds maximum of 50MB')
        
        # Validate image dimensions
        if self.file_type == 'image' and self.width and self.height:
            if self.width > 10000 or self.height > 10000:
                raise ValidationError('Image dimensions too large')
    
    def __str__(self):
        return f"{self.file_name} ({self.file_type})"
