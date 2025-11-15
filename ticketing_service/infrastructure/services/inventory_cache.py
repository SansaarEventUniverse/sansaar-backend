import uuid
import redis
from typing import Optional
from django.conf import settings


class TicketInventoryCache:
    """Redis-based ticket inventory tracking."""
    
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True
        )
    
    def get_available_count(self, ticket_type_id: uuid.UUID) -> Optional[int]:
        """Get available ticket count from cache."""
        key = f"ticket:inventory:{ticket_type_id}"
        count = self.redis_client.get(key)
        return int(count) if count else None
    
    def set_available_count(self, ticket_type_id: uuid.UUID, count: int, ttl: int = 3600) -> None:
        """Set available ticket count in cache."""
        key = f"ticket:inventory:{ticket_type_id}"
        self.redis_client.setex(key, ttl, count)
    
    def decrement_count(self, ticket_type_id: uuid.UUID, quantity: int) -> int:
        """Decrement available ticket count."""
        key = f"ticket:inventory:{ticket_type_id}"
        return self.redis_client.decrby(key, quantity)
    
    def increment_count(self, ticket_type_id: uuid.UUID, quantity: int) -> int:
        """Increment available ticket count."""
        key = f"ticket:inventory:{ticket_type_id}"
        return self.redis_client.incrby(key, quantity)
    
    def delete_cache(self, ticket_type_id: uuid.UUID) -> None:
        """Delete ticket inventory cache."""
        key = f"ticket:inventory:{ticket_type_id}"
        self.redis_client.delete(key)
