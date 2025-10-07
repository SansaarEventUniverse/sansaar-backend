import json
import pika
from django.conf import settings


class RabbitMQConsumer:
    def __init__(self):
        self.connection = None
        self.channel = None

    def connect(self):
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
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def consume(self, queue_name, callback):
        self.channel.queue_declare(queue=queue_name, durable=True)
        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=callback,
            auto_ack=True
        )
        self.channel.start_consuming()

    def close(self):
        if self.connection:
            self.connection.close()
