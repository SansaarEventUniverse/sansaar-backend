import json
import pika
from django.conf import settings


class RabbitMQConsumer:
    def __init__(self):
        credentials = pika.PlainCredentials(
            settings.RABBITMQ_USER,
            settings.RABBITMQ_PASSWORD
        )
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=settings.RABBITMQ_HOST,
                port=settings.RABBITMQ_PORT,
                credentials=credentials
            )
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='user_registered', durable=True)

    def callback(self, ch, method, properties, body):
        data = json.loads(body)
        print(f"Received UserRegistered event: {data}")
        # TODO: Handle user registration event
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        self.channel.basic_consume(
            queue='user_registered',
            on_message_callback=self.callback
        )
        print('Waiting for UserRegistered events...')
        self.channel.start_consuming()

    def close(self):
        self.connection.close()
