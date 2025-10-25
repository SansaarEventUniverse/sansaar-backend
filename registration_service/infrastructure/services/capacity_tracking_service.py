import redis
from django.conf import settings
import uuid


class CapacityTrackingService:
    """Service for tracking event capacity in Redis."""
    
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None,
            decode_responses=True
        )
    
    def increment_capacity(self, event_id: uuid.UUID) -> int:
        """Increment registered count for event."""
        key = f"event:{event_id}:registered"
        return self.redis_client.incr(key)
    
    def decrement_capacity(self, event_id: uuid.UUID) -> int:
        """Decrement registered count for event."""
        key = f"event:{event_id}:registered"
        return self.redis_client.decr(key)
    
    def get_registered_count(self, event_id: uuid.UUID) -> int:
        """Get current registered count."""
        key = f"event:{event_id}:registered"
        count = self.redis_client.get(key)
        return int(count) if count else 0
    
    def check_capacity(self, event_id: uuid.UUID, max_capacity: int) -> bool:
        """Check if event has available capacity."""
        registered = self.get_registered_count(event_id)
        return registered < max_capacity
