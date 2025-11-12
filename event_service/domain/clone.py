import uuid
from django.db import models


class EventClone(models.Model):
    """Model for tracking event clones."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Original and cloned event
    original_event_id = models.UUIDField(db_index=True)
    cloned_event_id = models.UUIDField(unique=True)
    
    # Clone metadata
    cloned_by = models.UUIDField()
    clone_reason = models.CharField(max_length=255, blank=True)
    
    # Customization tracking
    fields_modified = models.JSONField(default=list)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'event_clones'
        indexes = [
            models.Index(fields=['original_event_id']),
            models.Index(fields=['cloned_by']),
        ]
    
    def __str__(self):
        return f"Clone of {self.original_event_id}"
