import uuid
from django.db import models


class UserPreference(models.Model):
    """User preference model for personalized recommendations."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(unique=True)
    
    # Preferred categories (stored as JSON array)
    preferred_categories = models.JSONField(default=list)
    preferred_tags = models.JSONField(default=list)
    
    # Location preferences
    preferred_cities = models.JSONField(default=list)
    max_distance_km = models.FloatField(default=50.0)
    
    # Interaction history
    viewed_events = models.JSONField(default=list)
    registered_events = models.JSONField(default=list)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_preferences'
        indexes = [
            models.Index(fields=['user_id']),
        ]
    
    def add_viewed_event(self, event_id: uuid.UUID) -> None:
        """Add event to viewed history."""
        event_str = str(event_id)
        if event_str not in self.viewed_events:
            self.viewed_events.append(event_str)
            # Keep only last 50
            self.viewed_events = self.viewed_events[-50:]
            self.save()
    
    def add_registered_event(self, event_id: uuid.UUID) -> None:
        """Add event to registered history."""
        event_str = str(event_id)
        if event_str not in self.registered_events:
            self.registered_events.append(event_str)
            self.save()
    
    def __str__(self):
        return f"Preferences for user {self.user_id}"


class RecommendationScore(models.Model):
    """Recommendation score for event-user pairs."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField()
    event_id = models.UUIDField()
    
    # Scoring components
    category_score = models.FloatField(default=0.0)
    tag_score = models.FloatField(default=0.0)
    location_score = models.FloatField(default=0.0)
    popularity_score = models.FloatField(default=0.0)
    
    # Final score
    total_score = models.FloatField(default=0.0)
    
    # Metadata
    reason = models.CharField(max_length=255, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'recommendation_scores'
        unique_together = [['user_id', 'event_id']]
        indexes = [
            models.Index(fields=['user_id', '-total_score']),
            models.Index(fields=['event_id']),
        ]
    
    def calculate_total_score(self) -> float:
        """Calculate weighted total score."""
        # Weights for different components
        weights = {
            'category': 0.3,
            'tag': 0.25,
            'location': 0.25,
            'popularity': 0.2,
        }
        
        self.total_score = (
            self.category_score * weights['category'] +
            self.tag_score * weights['tag'] +
            self.location_score * weights['location'] +
            self.popularity_score * weights['popularity']
        )
        return self.total_score
    
    def __str__(self):
        return f"Score {self.total_score:.2f} for event {self.event_id}"
