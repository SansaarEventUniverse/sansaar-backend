import pika
import json
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
    
    def setup_queues(self):
        self.channel.queue_declare(queue='analytics_events', durable=True)
    
    def callback(self, ch, method, properties, body):
        try:
            data = json.loads(body)
            print(f"Received analytics event: {data}")
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"Error processing message: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    
    def start_consuming(self):
        self.connect()
        self.setup_queues()
        self.channel.basic_consume(
            queue='analytics_events',
            on_message_callback=self.callback
        )
        print('Analytics service waiting for messages...')
        self.channel.start_consuming()
    
    def close(self):
        if self.connection:
            self.connection.close()
