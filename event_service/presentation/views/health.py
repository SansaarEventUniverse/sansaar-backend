import boto3
import redis
from django.conf import settings
from django.db import connection
from elasticsearch import Elasticsearch
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def health_check(request):
    """Health check endpoint to verify all service connections"""
    health_status = {
        "service": "event_service",
        "status": "healthy",
        "checks": {}
    }

    # Check PostgreSQL
    try:
        connection.ensure_connection()
        health_status["checks"]["postgresql"] = "connected"
    except Exception as e:
        health_status["checks"]["postgresql"] = f"error: {str(e)}"
        health_status["status"] = "unhealthy"

    # Check Redis
    try:
        r = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None
        )
        r.ping()
        health_status["checks"]["redis"] = "connected"
    except Exception as e:
        health_status["checks"]["redis"] = f"error: {str(e)}"
        health_status["status"] = "unhealthy"

    # Check Elasticsearch
    try:
        es = Elasticsearch([f"http://{settings.ELASTICSEARCH_HOST}:{settings.ELASTICSEARCH_PORT}"])
        es.ping()
        health_status["checks"]["elasticsearch"] = "connected"
    except Exception as e:
        health_status["checks"]["elasticsearch"] = f"error: {str(e)}"
        health_status["status"] = "unhealthy"

    # Check AWS S3
    try:
        s3_config = {
            'aws_access_key_id': settings.AWS_ACCESS_KEY_ID,
            'aws_secret_access_key': settings.AWS_SECRET_ACCESS_KEY,
            'region_name': settings.AWS_REGION
        }
        if settings.AWS_S3_ENDPOINT_URL:
            s3_config['endpoint_url'] = settings.AWS_S3_ENDPOINT_URL
        
        s3 = boto3.client('s3', **s3_config)
        s3.head_bucket(Bucket=settings.AWS_S3_BUCKET_NAME)
        health_status["checks"]["s3"] = "connected"
    except Exception as e:
        health_status["checks"]["s3"] = f"error: {str(e)}"
        health_status["status"] = "unhealthy"

    # Check RabbitMQ
    try:
        from event_service.celery import app
        app.connection().ensure_connection(max_retries=1)
        health_status["checks"]["rabbitmq"] = "connected"
    except Exception as e:
        health_status["checks"]["rabbitmq"] = f"error: {str(e)}"
        health_status["status"] = "unhealthy"

    status_code = 200 if health_status["status"] == "healthy" else 503
    return Response(health_status, status=status_code)
