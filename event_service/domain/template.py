import uuid
from django.db import models
from django.core.exceptions import ValidationError


class EventTemplate(models.Model):
    """Event template model for reusable event configurations."""
    
    CATEGORY_CHOICES = [
        ('conference', 'Conference'),
        ('workshop', 'Workshop'),
        ('meetup', 'Meetup'),
        ('webinar', 'Webinar'),
        ('social', 'Social Event'),
        ('sports', 'Sports Event'),
        ('other', 'Other'),
    ]
    
    VISIBILITY_CHOICES = [
        ('private', 'Private'),
        ('organization', 'Organization'),
        ('public', 'Public'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Template info
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=2000)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    
    # Template data (JSON)
    template_data = models.JSONField(default=dict)
    
    # Ownership
    created_by = models.UUIDField()
    organization_id = models.UUIDField(null=True, blank=True)
    
    # Visibility
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='private')
    is_featured = models.BooleanField(default=False)
    
    # Versioning
    version = models.IntegerField(default=1)
    parent_template_id = models.UUIDField(null=True, blank=True)
    
    # Usage tracking
    usage_count = models.IntegerField(default=0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'event_templates'
        indexes = [
            models.Index(fields=['category', 'visibility']),
            models.Index(fields=['created_by']),
            models.Index(fields=['organization_id']),
            models.Index(fields=['is_featured']),
        ]
    
    def validate_template_data(self) -> None:
        """Validate template data structure."""
        required_fields = ['title', 'description']
        for field in required_fields:
            if field not in self.template_data:
                raise ValidationError(f"Template data missing required field: {field}")
    
    def can_access(self, user_id: uuid.UUID, org_id: uuid.UUID = None) -> bool:
        """Check if user can access template."""
        if self.visibility == 'public':
            return True
        if self.visibility == 'organization' and org_id == self.organization_id:
            return True
        if self.created_by == user_id:
            return True
        return False
    
    def increment_usage(self) -> None:
        """Increment usage count."""
        self.usage_count += 1
        self.save(update_fields=['usage_count'])
    
    def create_new_version(self, updated_data: dict, updated_by: uuid.UUID) -> 'EventTemplate':
        """Create new version of template."""
        new_template = EventTemplate.objects.create(
            name=self.name,
            description=self.description,
            category=self.category,
            template_data=updated_data,
            created_by=updated_by,
            organization_id=self.organization_id,
            visibility=self.visibility,
            version=self.version + 1,
            parent_template_id=self.id,
        )
        return new_template
    
    def clone_template(self, cloned_by: uuid.UUID, new_name: str = None) -> 'EventTemplate':
        """Clone template for customization."""
        return EventTemplate.objects.create(
            name=new_name or f"{self.name} (Copy)",
            description=self.description,
            category=self.category,
            template_data=self.template_data.copy(),
            created_by=cloned_by,
            visibility='private',
            parent_template_id=self.id,
        )
    
    def __str__(self):
        return f"{self.name} (v{self.version})"
