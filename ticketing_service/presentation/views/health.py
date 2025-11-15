import redis
import pika
from django.db import connection
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
def health_check(request):
    """Health check endpoint to verify all services are running."""
    health_status = {
        'service': 'ticketing_service',
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
            db=settings.REDIS_DB
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
    
    status_code = status.HTTP_200_OK if health_status['status'] == 'healthy' else status.HTTP_503_SERVICE_UNAVAILABLE
    return Response(health_status, status=status_code)
