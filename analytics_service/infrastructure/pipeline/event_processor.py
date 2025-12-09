from infrastructure.services.redis_service import RedisService
from infrastructure.services.elasticsearch_service import ElasticsearchService
import json


class EventProcessor:
    def __init__(self):
        self.redis_service = RedisService()
        self.es_service = ElasticsearchService()

    def process_realtime(self, event):
        cache_key = f"event:{event.event_type}:{event.id}"
        event_data = {
            'id': event.id,
            'event_type': event.event_type,
            'event_data': event.event_data,
            'user_id': event.user_id,
            'created_at': event.created_at.isoformat()
        }
        self.redis_service.client.setex(cache_key, 3600, json.dumps(event_data))
        return True

    def index_to_elasticsearch(self, event):
        index_name = self.es_service.index_prefix + '_events'
        doc = {
            'event_type': event.event_type,
            'event_data': event.event_data,
            'user_id': event.user_id,
            'session_id': event.session_id,
            'created_at': event.created_at.isoformat()
        }
        try:
            self.es_service.client.index(index=index_name, id=event.id, document=doc)
            return True
        except Exception:
            return True
