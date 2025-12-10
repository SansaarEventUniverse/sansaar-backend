import redis
import json
from django.conf import settings


class RedisService:
    def __init__(self):
        self.client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None,
            decode_responses=True
        )
    
    def set(self, key, value, expiry=None):
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        return self.client.set(key, value, ex=expiry)
    
    def get(self, key):
        value = self.client.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        return None
    
    def delete(self, key):
        return self.client.delete(key)
    
    def exists(self, key):
        return self.client.exists(key)
    
    def increment(self, key, amount=1):
        return self.client.incr(key, amount)
    
    def expire(self, key, seconds):
        return self.client.expire(key, seconds)
