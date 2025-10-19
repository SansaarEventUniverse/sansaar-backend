import uuid
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from unittest.mock import patch, MagicMock

from infrastructure.services.event_publisher import EventPublisher
from domain.event import Event


class EventPublisherTest(TestCase):
    """Tests for EventPublisher."""
    
    def setUp(self):
        self.publisher = EventPublisher()
        self.organizer_id = uuid.uuid4()
        self.venue_id = uuid.uuid4()
        self.now = timezone.now()
        self.event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            organizer_id=self.organizer_id,
            start_datetime=self.now + timedelta(days=1),
            end_datetime=self.now + timedelta(days=2),
            venue_id=self.venue_id,
        )
        
    @patch('infrastructure.services.event_publisher.pika.BlockingConnection')
    def test_publish_event_created(self, mock_connection):
        """Test publishing event.created."""
        mock_channel = MagicMock()
        mock_connection.return_value.channel.return_value = mock_channel
        
        self.publisher.publish_event_created(self.event)
        
        mock_channel.basic_publish.assert_called_once()
        call_args = mock_channel.basic_publish.call_args
        self.assertEqual(call_args[1]['routing_key'], 'event.created')
        
    @patch('infrastructure.services.event_publisher.pika.BlockingConnection')
    def test_publish_event_updated(self, mock_connection):
        """Test publishing event.updated."""
        mock_channel = MagicMock()
        mock_connection.return_value.channel.return_value = mock_channel
        
        self.publisher.publish_event_updated(self.event)
        
        mock_channel.basic_publish.assert_called_once()
        call_args = mock_channel.basic_publish.call_args
        self.assertEqual(call_args[1]['routing_key'], 'event.updated')
        
    @patch('infrastructure.services.event_publisher.pika.BlockingConnection')
    def test_publish_event_published(self, mock_connection):
        """Test publishing event.published."""
        mock_channel = MagicMock()
        mock_connection.return_value.channel.return_value = mock_channel
        
        self.publisher.publish_event_published(self.event)
        
        mock_channel.basic_publish.assert_called_once()
        call_args = mock_channel.basic_publish.call_args
        self.assertEqual(call_args[1]['routing_key'], 'event.published')
        
    @patch('infrastructure.services.event_publisher.pika.BlockingConnection')
    def test_publish_event_cancelled(self, mock_connection):
        """Test publishing event.cancelled."""
        mock_channel = MagicMock()
        mock_connection.return_value.channel.return_value = mock_channel
        
        self.publisher.publish_event_cancelled(self.event)
        
        mock_channel.basic_publish.assert_called_once()
        call_args = mock_channel.basic_publish.call_args
        self.assertEqual(call_args[1]['routing_key'], 'event.cancelled')
