import pika
from django.db import connection
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from infrastructure.services.stripe_client import StripeClient
from infrastructure.services.paypal_client import PayPalClient
from infrastructure.services.esewa_client import ESewaClient
from infrastructure.services.khalti_client import KhaltiClient


@api_view(['GET'])
def health_check(request):
    """Health check endpoint to verify all services and payment gateways."""
    health_status = {
        'service': 'payment_service',
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
    
    # Check Stripe
    try:
        stripe_client = StripeClient()
        stripe_client.check_connection()
        health_status['checks']['stripe'] = 'connected'
    except Exception as e:
        health_status['checks']['stripe'] = f'error: {str(e)}'
        health_status['status'] = 'degraded'
    
    # Check PayPal
    try:
        paypal_client = PayPalClient()
        paypal_client.check_connection()
        health_status['checks']['paypal'] = 'connected'
    except Exception as e:
        health_status['checks']['paypal'] = f'error: {str(e)}'
        health_status['status'] = 'degraded'
    
    # Check eSewa
    try:
        esewa_client = ESewaClient()
        esewa_client.check_connection()
        health_status['checks']['esewa'] = 'connected'
    except Exception as e:
        health_status['checks']['esewa'] = f'error: {str(e)}'
        health_status['status'] = 'degraded'
    
    # Check Khalti
    try:
        khalti_client = KhaltiClient()
        khalti_client.check_connection()
        health_status['checks']['khalti'] = 'connected'
    except Exception as e:
        health_status['checks']['khalti'] = f'error: {str(e)}'
        health_status['status'] = 'degraded'
    
    status_code = status.HTTP_200_OK if health_status['status'] in ['healthy', 'degraded'] else status.HTTP_503_SERVICE_UNAVAILABLE
    return Response(health_status, status=status_code)
