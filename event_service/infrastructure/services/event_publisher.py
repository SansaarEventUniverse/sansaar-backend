import json
import pika
from django.conf import settings

from domain.event import Event


class EventPublisher:
    """Publisher for event domain events via RabbitMQ."""
    
    def __init__(self):
        self.connection = None
        self.channel = None
    
    def _connect(self):
        """Establish RabbitMQ connection."""
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
        self.channel.exchange_declare(
            exchange='events',
            exchange_type='topic',
            durable=True
        )
    
    def _close(self):
        """Close RabbitMQ connection."""
        if self.connection and not self.connection.is_closed:
            self.connection.close()
    
    def publish_event_created(self, event: Event):
        """Publish event.created event."""
        self._publish('event.created', {
            'event_id': str(event.id),
            'organizer_id': str(event.organizer_id),
            'organization_id': str(event.organization_id) if event.organization_id else None,
            'title': event.title,
            'start_datetime': event.start_datetime.isoformat(),
            'end_datetime': event.end_datetime.isoformat(),
        })
    
    def publish_event_updated(self, event: Event):
        """Publish event.updated event."""
        self._publish('event.updated', {
            'event_id': str(event.id),
            'organizer_id': str(event.organizer_id),
            'title': event.title,
        })
    
    def publish_event_published(self, event: Event):
        """Publish event.published event."""
        self._publish('event.published', {
            'event_id': str(event.id),
            'organizer_id': str(event.organizer_id),
            'title': event.title,
        })
    
    def publish_event_cancelled(self, event: Event):
        """Publish event.cancelled event."""
        self._publish('event.cancelled', {
            'event_id': str(event.id),
            'organizer_id': str(event.organizer_id),
            'title': event.title,
        })
    
    def _publish(self, routing_key: str, message: dict):
        """Publish message to RabbitMQ."""
        try:
            self._connect()
            self.channel.basic_publish(
                exchange='events',
                routing_key=routing_key,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # persistent
                    content_type='application/json'
                )
            )
        finally:
            self._close()
