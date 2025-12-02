import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "user_org_service.settings")

app = Celery("user_org_service")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task(bind=True)
def start_rabbitmq_consumer(self):
    """Start RabbitMQ consumer for user registration events"""
    from infrastructure.messaging.rabbitmq_consumer import RabbitMQConsumer

    consumer = RabbitMQConsumer()
    consumer.start_consuming()

