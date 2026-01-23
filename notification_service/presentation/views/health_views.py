from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection
from infrastructure.cache.redis_cache import RedisCache
import pika
from django.conf import settings

@api_view(['GET'])
def health_check(request):
    status = {'status': 'healthy', 'services': {}}
    
    try:
        connection.ensure_connection()
        status['services']['postgresql'] = 'connected'
    except Exception:
        status['services']['postgresql'] = 'disconnected'
        status['status'] = 'unhealthy'
    
    try:
        cache = RedisCache()
        cache.set('health_check', 'ok', 10)
        status['services']['redis'] = 'connected'
    except Exception:
        status['services']['redis'] = 'disconnected'
        status['status'] = 'unhealthy'
    
    try:
        credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
        conn = pika.BlockingConnection(pika.ConnectionParameters(settings.RABBITMQ_HOST, settings.RABBITMQ_PORT, credentials=credentials))
        conn.close()
        status['services']['rabbitmq'] = 'connected'
    except Exception:
        status['services']['rabbitmq'] = 'disconnected'
        status['status'] = 'unhealthy'
    
    status['services']['firebase'] = 'configured' if settings.FIREBASE_CREDENTIALS_PATH else 'not_configured'
    status['services']['websocket'] = 'enabled'
    
    return Response(status)
