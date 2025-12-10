from domain.models import AnalyticsEvent
from infrastructure.services.redis_service import RedisService
import json


class RealTimeAnalyticsService:
    def __init__(self):
        self.redis_service = RedisService()

    def get_realtime_metrics(self):
        total = AnalyticsEvent.objects.count()
        unprocessed = AnalyticsEvent.objects.filter(is_processed=False).count()
        return {
            'total_events': total,
            'unprocessed_events': unprocessed,
            'processed_events': total - unprocessed
        }

    def cache_realtime_data(self, key, data, ttl=300):
        self.redis_service.client.setex(key, ttl, json.dumps(data))

    def get_cached_data(self, key):
        data = self.redis_service.client.get(key)
        return json.loads(data) if data else None
