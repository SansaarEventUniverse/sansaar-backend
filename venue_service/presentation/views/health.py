from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from django.db import connection
import redis
import pika
import googlemaps


@api_view(['GET'])
def health_check(request):
    """Health check endpoint for venue_service."""
    health_status = {
        'service': 'venue_service',
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
    
    # Check Google Maps API
    try:
        gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
        # Simple validation - just check if key is set
        if settings.GOOGLE_MAPS_API_KEY and settings.GOOGLE_MAPS_API_KEY != 'your-google-maps-api-key':
            health_status['checks']['google_maps'] = 'configured'
        else:
            health_status['checks']['google_maps'] = 'not configured'
    except Exception as e:
        health_status['checks']['google_maps'] = f'error: {str(e)}'
    
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
