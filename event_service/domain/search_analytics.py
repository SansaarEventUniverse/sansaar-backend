import uuid
from django.db import models


class SearchQuery(models.Model):
    """Model for tracking search queries."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Query details
    query_text = models.CharField(max_length=255)
    filters = models.JSONField(default=dict)
    
    # Results
    result_count = models.IntegerField(default=0)
    
    # Performance
    response_time_ms = models.IntegerField(default=0)
    
    # User context
    user_id = models.UUIDField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'search_queries'
        indexes = [
            models.Index(fields=['query_text']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['user_id']),
        ]
    
    def __str__(self):
        return f"{self.query_text} ({self.result_count} results)"


class SearchAnalytics(models.Model):
    """Aggregated search analytics model."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Time period
    date = models.DateField()
    
    # Metrics
    total_searches = models.IntegerField(default=0)
    unique_queries = models.IntegerField(default=0)
    avg_response_time_ms = models.FloatField(default=0.0)
    
    # Popular queries (top 10)
    popular_queries = models.JSONField(default=list)
    
    # Zero result queries
    zero_result_queries = models.JSONField(default=list)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'search_analytics'
        unique_together = [['date']]
        indexes = [
            models.Index(fields=['-date']),
        ]
    
    def calculate_metrics(self, queries) -> None:
        """Calculate metrics from queries."""
        self.total_searches = len(queries)
        self.unique_queries = len(set(q.query_text for q in queries))
        
        if queries:
            self.avg_response_time_ms = sum(q.response_time_ms for q in queries) / len(queries)
        
        # Get popular queries
        query_counts = {}
        for q in queries:
            query_counts[q.query_text] = query_counts.get(q.query_text, 0) + 1
        
        self.popular_queries = [
            {'query': k, 'count': v}
            for k, v in sorted(query_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        ]
        
        # Get zero result queries
        zero_results = [q.query_text for q in queries if q.result_count == 0]
        self.zero_result_queries = list(set(zero_results))[:10]
    
    def __str__(self):
        return f"Analytics for {self.date}"
