import pika
from django.conf import settings

class RabbitMQPublisher:
    def __init__(self):
        self.connection = None
        self.channel = None
    
    def connect(self):
        credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
        parameters = pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            virtual_host=settings.RABBITMQ_VHOST,
            credentials=credentials
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
    
    def publish(self, exchange, routing_key, message):
        if not self.channel:
            self.connect()
        self.channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message)
    
    def close(self):
        if self.connection:
            self.connection.close()
