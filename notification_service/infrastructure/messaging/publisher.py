import pika
import json
from django.conf import settings

class RabbitMQPublisher:
    def __init__(self):
        credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST, port=settings.RABBITMQ_PORT, credentials=credentials))
        self.channel = self.connection.channel()

    def publish(self, queue, message):
        self.channel.queue_declare(queue=queue, durable=True)
        self.channel.basic_publish(exchange='', routing_key=queue, body=json.dumps(message))

    def close(self):
        self.connection.close()
