import json

import pika
from django.conf import settings

from infrastructure.messaging.user_registered_event_handler import UserRegisteredEventHandler


class RabbitMQConsumer:
    def __init__(self):
        credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=settings.RABBITMQ_HOST, port=settings.RABBITMQ_PORT, credentials=credentials)
        )
        self.channel = self.connection.channel()
        
        # Declare exchange
        self.channel.exchange_declare(exchange="auth_events", exchange_type="topic", durable=True)
        
        # Declare queue
        self.channel.queue_declare(queue="user_registered", durable=True)
        
        # Bind queue to exchange with routing key
        self.channel.queue_bind(exchange="auth_events", queue="user_registered", routing_key="user.registered")
        
        self.handler = UserRegisteredEventHandler()

    def callback(self, ch, method, properties, body):
        data = json.loads(body)
        print(f"Received UserRegistered event: {data}")
        self.handler.handle(data)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        self.channel.basic_consume(queue="user_registered", on_message_callback=self.callback)
        print("Waiting for UserRegistered events...")
        self.channel.start_consuming()

    def close(self):
        self.connection.close()
