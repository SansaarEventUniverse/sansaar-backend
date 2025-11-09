import uuid
from django.db import models
from django.core.exceptions import ValidationError


class Document(models.Model):
    """Document model for event documents."""
    
    DOCUMENT_TYPES = [
        ('agenda', 'Agenda'),
        ('schedule', 'Schedule'),
        ('guidelines', 'Guidelines'),
        ('terms', 'Terms & Conditions'),
        ('waiver', 'Waiver'),
        ('other', 'Other'),
    ]
    
    ACCESS_LEVELS = [
        ('public', 'Public'),
        ('registered', 'Registered Only'),
        ('organizer', 'Organizer Only'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_id = models.UUIDField(db_index=True)
    
    # Document info
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    
    # File info
    file_name = models.CharField(max_length=255)
    file_size = models.BigIntegerField()
    mime_type = models.CharField(max_length=100)
    s3_key = models.CharField(max_length=500)
    
    # Access control
    access_level = models.CharField(max_length=20, choices=ACCESS_LEVELS, default='public')
    is_required = models.BooleanField(default=False)
    
    # Versioning
    version = models.IntegerField(default=1)
    previous_version_id = models.UUIDField(null=True, blank=True)
    
    # Security
    is_encrypted = models.BooleanField(default=False)
    is_scanned = models.BooleanField(default=False)
    
    # Metadata
    download_count = models.IntegerField(default=0)
    created_by = models.UUIDField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'documents'
        indexes = [
            models.Index(fields=['event_id', 'document_type']),
            models.Index(fields=['access_level']),
        ]
    
    def validate_file_size(self) -> None:
        """Validate file size (100MB max)."""
        MAX_SIZE = 100 * 1024 * 1024
        if self.file_size > MAX_SIZE:
            raise ValidationError(f"File size exceeds maximum of {MAX_SIZE} bytes")
    
    def can_access(self, user_role: str) -> bool:
        """Check if user can access document."""
        if self.access_level == 'public':
            return True
        if self.access_level == 'registered' and user_role in ['registered', 'organizer']:
            return True
        if self.access_level == 'organizer' and user_role == 'organizer':
            return True
        return False
    
    def increment_downloads(self) -> None:
        """Increment download count."""
        self.download_count += 1
        self.save(update_fields=['download_count'])
    
    def create_new_version(self, new_s3_key: str, new_file_size: int) -> 'Document':
        """Create new version of document."""
        new_doc = Document.objects.create(
            event_id=self.event_id,
            title=self.title,
            description=self.description,
            document_type=self.document_type,
            file_name=self.file_name,
            file_size=new_file_size,
            mime_type=self.mime_type,
            s3_key=new_s3_key,
            access_level=self.access_level,
            is_required=self.is_required,
            version=self.version + 1,
            previous_version_id=self.id,
            is_encrypted=self.is_encrypted,
            created_by=self.created_by,
        )
        return new_doc
    
    def __str__(self):
        return f"{self.title} (v{self.version})"
