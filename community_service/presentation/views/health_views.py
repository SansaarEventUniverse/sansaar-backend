from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection
from infrastructure.cache.redis_cache import RedisCache
from infrastructure.messaging.publisher import RabbitMQPublisher

@api_view(['GET'])
def health_check(request):
    status = {'status': 'healthy', 'services': {}}
    
    # Check PostgreSQL
    try:
        connection.ensure_connection()
        status['services']['postgresql'] = 'connected'
    except Exception as e:
        status['services']['postgresql'] = f'error: {str(e)}'
        status['status'] = 'unhealthy'
    
    # Check Redis
    try:
        cache = RedisCache()
        cache.set('health_check', 'ok', ttl=10)
        if cache.get('health_check') == 'ok':
            status['services']['redis'] = 'connected'
        else:
            status['services']['redis'] = 'error'
            status['status'] = 'unhealthy'
    except Exception as e:
        status['services']['redis'] = f'error: {str(e)}'
        status['status'] = 'unhealthy'
    
    # Check RabbitMQ
    try:
        publisher = RabbitMQPublisher()
        publisher.connect()
        publisher.close()
        status['services']['rabbitmq'] = 'connected'
    except Exception as e:
        status['services']['rabbitmq'] = f'error: {str(e)}'
        status['status'] = 'unhealthy'
    
    return Response(status)
