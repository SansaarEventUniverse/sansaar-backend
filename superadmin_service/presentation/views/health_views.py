from django.conf import settings
from django.db import connection
from django.http import JsonResponse
from elasticsearch import Elasticsearch


def health_check(request):
    health_status = {"status": "healthy", "services": {}}

    try:
        connection.ensure_connection()
        health_status["services"]["postgresql"] = "connected"
    except Exception:
        health_status["services"]["postgresql"] = "disconnected"
        health_status["status"] = "unhealthy"

    try:
        es = Elasticsearch([f"http://{settings.ELASTICSEARCH_HOST}:{settings.ELASTICSEARCH_PORT}"])
        if es.ping():
            health_status["services"]["elasticsearch"] = "connected"
        else:
            health_status["services"]["elasticsearch"] = "disconnected"
            health_status["status"] = "unhealthy"
    except Exception:
        health_status["services"]["elasticsearch"] = "disconnected"
        health_status["status"] = "unhealthy"

    if settings.SENTRY_DSN:
        health_status["services"]["sentry"] = "configured"
    else:
        health_status["services"]["sentry"] = "not configured"

    return JsonResponse(health_status)
