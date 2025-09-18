import sentry_sdk
from celery import current_app
from django.core.cache import cache
from django.db import connection
from rest_framework.decorators import api_view
from rest_framework.response import Response


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
        cache.set('health_check', 'ok', 10)
        if cache.get('health_check') == 'ok':
            status['services']['redis'] = 'connected'
        else:
            status['services']['redis'] = 'error: cache test failed'
            status['status'] = 'unhealthy'
    except Exception as e:
        status['services']['redis'] = f'error: {str(e)}'
        status['status'] = 'unhealthy'

    # Check Celery
    try:
        inspect = current_app.control.inspect()
        if inspect.ping():
            status['services']['celery'] = 'connected'
        else:
            status['services']['celery'] = 'no workers available'
    except Exception as e:
        status['services']['celery'] = f'error: {str(e)}'

    # Check Sentry
    try:
        client = sentry_sdk.Hub.current.client
        if client and client.dsn:
            status['services']['sentry'] = 'configured'
        else:
            status['services']['sentry'] = 'not configured'
    except Exception as e:
        status['services']['sentry'] = f'error: {str(e)}'

    return Response(status)
