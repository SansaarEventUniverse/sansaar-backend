from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db import connection
from infrastructure.cache.cache_service import CacheService
import pika
from django.conf import settings


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    health_status = {
        'status': 'healthy',
        'services': {}
    }

    try:
        connection.ensure_connection()
        health_status['services']['postgresql'] = 'connected'
    except Exception:
        health_status['services']['postgresql'] = 'disconnected'
        health_status['status'] = 'unhealthy'

    try:
        cache = CacheService()
        cache.client.ping()
        health_status['services']['redis'] = 'connected'
    except Exception:
        health_status['services']['redis'] = 'disconnected'
        health_status['status'] = 'unhealthy'

    try:
        credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
        parameters = pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            virtual_host=settings.RABBITMQ_VHOST,
            credentials=credentials
        )
        conn = pika.BlockingConnection(parameters)
        conn.close()
        health_status['services']['rabbitmq'] = 'connected'
    except Exception:
        health_status['services']['rabbitmq'] = 'disconnected'
        health_status['status'] = 'unhealthy'

    health_status['services']['sentry'] = 'configured' if settings.SENTRY_DSN else 'not configured'

    return Response(health_status)
