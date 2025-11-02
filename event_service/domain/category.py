import uuid
from django.db import models
from django.core.exceptions import ValidationError


class Category(models.Model):
    """Category model with hierarchical support."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    # Hierarchy
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    
    # Metadata
    is_active = models.BooleanField(default=True)
    event_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'categories'
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['parent']),
        ]
    
    def clean(self):
        """Validate category."""
        if self.parent == self:
            raise ValidationError('Category cannot be its own parent')
        
        # Check for circular reference
        if self.parent:
            current = self.parent
            while current:
                if current == self:
                    raise ValidationError('Circular parent reference detected')
                current = current.parent
    
    def get_ancestors(self):
        """Get all ancestor categories."""
        ancestors = []
        current = self.parent
        while current:
            ancestors.append(current)
            current = current.parent
        return ancestors
    
    def get_descendants(self):
        """Get all descendant categories."""
        descendants = list(self.children.all())
        for child in self.children.all():
            descendants.extend(child.get_descendants())
        return descendants
    
    def __str__(self):
        return self.name


class Tag(models.Model):
    """Tag model for flexible event tagging."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    
    # Metadata
    usage_count = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'tags'
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['-usage_count']),
        ]
        ordering = ['-usage_count']
    
    def increment_usage(self):
        """Increment usage count."""
        self.usage_count += 1
        self.save()
    
    def __str__(self):
        return self.name
