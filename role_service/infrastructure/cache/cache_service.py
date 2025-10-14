import redis
from django.conf import settings


class CacheService:
    def __init__(self):
        self.client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True
        )
        self.ttl = settings.PERMISSION_CACHE_TTL

    def get(self, key):
        return self.client.get(key)

    def set(self, key, value):
        self.client.setex(key, self.ttl, value)

    def delete(self, key):
        self.client.delete(key)

    def clear_pattern(self, pattern):
        keys = self.client.keys(pattern)
        if keys:
            self.client.delete(*keys)
