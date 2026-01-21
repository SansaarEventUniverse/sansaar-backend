import redis
from django.conf import settings

class RedisCache:
    def __init__(self):
        self.client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True
        )

    def get(self, key):
        return self.client.get(key)

    def set(self, key, value, ttl=3600):
        self.client.setex(key, ttl, value)

    def delete(self, key):
        self.client.delete(key)
