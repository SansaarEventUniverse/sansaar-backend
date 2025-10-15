import json
import logging

import pika
from django.conf import settings

logger = logging.getLogger(__name__)


class EventPublisher:
    def __init__(self):
        self.host = settings.RABBITMQ_HOST
        self.port = settings.RABBITMQ_PORT
        self.user = settings.RABBITMQ_USER
        self.password = settings.RABBITMQ_PASSWORD

    def publish_user_registered(self, user_data):
        try:
            credentials = pika.PlainCredentials(self.user, self.password)
            parameters = pika.ConnectionParameters(host=self.host, port=self.port, credentials=credentials)

            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()

            channel.exchange_declare(exchange="auth_events", exchange_type="topic", durable=True)

            message = json.dumps(user_data)
            channel.basic_publish(
                exchange="auth_events",
                routing_key="user.registered",
                body=message,
                properties=pika.BasicProperties(delivery_mode=2),
            )

            connection.close()
            return True
        except Exception as e:
            logger.error(f"Failed to publish user registered event: {str(e)}")
            return False
