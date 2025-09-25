import pika
import redis
from celery import current_app
from django.conf import settings
from django.db import connection
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from infrastructure.storage.s3_service import S3Service


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    health_status = {
        'status': 'healthy',
        'services': {}
    }

    # Check PostgreSQL
    try:
        connection.ensure_connection()
        health_status['services']['postgresql'] = 'connected'
    except Exception as e:
        health_status['services']['postgresql'] = f'error: {str(e)}'
        health_status['status'] = 'unhealthy'

    # Check Redis
    try:
        r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
        r.ping()
        health_status['services']['redis'] = 'connected'
    except Exception as e:
        health_status['services']['redis'] = f'error: {str(e)}'
        health_status['status'] = 'unhealthy'

    # Check Celery
    try:
        inspect = current_app.control.inspect()
        stats = inspect.stats()
        if stats:
            health_status['services']['celery'] = 'connected'
        else:
            health_status['services']['celery'] = 'no workers'
    except Exception as e:
        health_status['services']['celery'] = f'error: {str(e)}'

    # Check RabbitMQ
    try:
        credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
        connection_params = pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            credentials=credentials
        )
        rabbitmq_connection = pika.BlockingConnection(connection_params)
        rabbitmq_connection.close()
        health_status['services']['rabbitmq'] = 'connected'
    except Exception as e:
        health_status['services']['rabbitmq'] = f'error: {str(e)}'
        health_status['status'] = 'unhealthy'

    # Check S3
    try:
        s3_service = S3Service()
        if s3_service.check_connection():
            health_status['services']['s3'] = 'connected'
        else:
            health_status['services']['s3'] = 'error'
            health_status['status'] = 'unhealthy'
    except Exception as e:
        health_status['services']['s3'] = f'error: {str(e)}'
        health_status['status'] = 'unhealthy'

    # Check Sentry
    if settings.SENTRY_DSN:
        health_status['services']['sentry'] = 'configured'
    else:
        health_status['services']['sentry'] = 'not configured'

    return Response(health_status, status=status.HTTP_200_OK)
