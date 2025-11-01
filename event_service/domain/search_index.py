import uuid
from django.db import models
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex


class EventSearchIndex(models.Model):
    """Search index model for event full-text search."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_id = models.UUIDField(unique=True)
    
    # Searchable fields
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100, blank=True)
    tags = models.JSONField(default=list)
    
    # Location fields
    location = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    
    # Status and visibility
    status = models.CharField(max_length=20, default='draft')
    is_published = models.BooleanField(default=False)
    
    # Search ranking
    search_rank = models.FloatField(default=0.0)
    view_count = models.IntegerField(default=0)
    
    # Full-text search vector
    search_vector = SearchVectorField(null=True)
    
    # Timestamps
    event_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'event_search_index'
        indexes = [
            models.Index(fields=['event_id']),
            models.Index(fields=['status', 'is_published']),
            models.Index(fields=['category']),
            models.Index(fields=['city']),
            models.Index(fields=['-search_rank']),
            GinIndex(fields=['search_vector']),
        ]
    
    def calculate_rank(self) -> float:
        """Calculate search ranking score."""
        rank = 0.0
        
        # Base rank from view count
        rank += self.view_count * 0.1
        
        # Boost for published events
        if self.is_published:
            rank += 10.0
        
        # Boost for events with tags
        rank += len(self.tags) * 0.5
        
        return round(rank, 2)
    
    def update_rank(self) -> None:
        """Update search rank."""
        self.search_rank = self.calculate_rank()
    
    def __str__(self):
        return f"{self.title} - Rank: {self.search_rank}"
