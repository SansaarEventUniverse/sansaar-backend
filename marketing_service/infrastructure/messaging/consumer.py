import pika
import json
from django.conf import settings

class RabbitMQConsumer:
    def __init__(self, queue):
        credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=settings.RABBITMQ_HOST, port=settings.RABBITMQ_PORT, credentials=credentials)
        )
        self.channel = self.connection.channel()
        self.queue = queue
        self.channel.queue_declare(queue=queue, durable=True)

    def consume(self, callback):
        def wrapper(ch, method, properties, body):
            message = json.loads(body)
            callback(message)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        
        self.channel.basic_consume(queue=self.queue, on_message_callback=wrapper)
        self.channel.start_consuming()
