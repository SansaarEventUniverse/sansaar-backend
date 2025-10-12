import pytest
from django.conf import settings
from django.test import Client
from elasticsearch import Elasticsearch


@pytest.mark.django_db
def test_health_check_postgresql():
    client = Client()
    response = client.get("/api/superadmin/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["services"]["postgresql"] == "connected"


def test_health_check_elasticsearch():
    client = Client()
    response = client.get("/api/superadmin/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["services"]["elasticsearch"] in ["connected", "disconnected"]


def test_elasticsearch_connection():
    es = Elasticsearch([f"http://{settings.ELASTICSEARCH_HOST}:{settings.ELASTICSEARCH_PORT}"])
    assert es.ping()
