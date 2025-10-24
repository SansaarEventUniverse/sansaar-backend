from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from django.db import connection
import redis
import pika


@api_view(['GET'])
def health_check(request):
    """Health check endpoint for registration_service."""
    health_status = {
        'service': 'registration_service',
        'status': 'healthy',
        'checks': {}
    }
    
    # Check PostgreSQL
    try:
        connection.ensure_connection()
        health_status['checks']['postgresql'] = 'connected'
    except Exception as e:
        health_status['checks']['postgresql'] = f'error: {str(e)}'
        health_status['status'] = 'unhealthy'
    
    # Check Redis
    try:
        r = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None
        )
        r.ping()
        health_status['checks']['redis'] = 'connected'
    except Exception as e:
        health_status['checks']['redis'] = f'error: {str(e)}'
        health_status['status'] = 'unhealthy'
    
    # Check RabbitMQ
    try:
        credentials = pika.PlainCredentials(
            settings.RABBITMQ_USER,
            settings.RABBITMQ_PASSWORD
        )
        parameters = pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            virtual_host=settings.RABBITMQ_VHOST,
            credentials=credentials
        )
        connection_rmq = pika.BlockingConnection(parameters)
        connection_rmq.close()
        health_status['checks']['rabbitmq'] = 'connected'
    except Exception as e:
        health_status['checks']['rabbitmq'] = f'error: {str(e)}'
        health_status['status'] = 'unhealthy'
    
    return Response(health_status)
