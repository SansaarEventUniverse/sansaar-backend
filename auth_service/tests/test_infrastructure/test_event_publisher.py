from unittest.mock import Mock, patch

from infrastructure.services.event_publisher import EventPublisher


class TestEventPublisher:
    def setup_method(self):
        self.publisher = EventPublisher()

    @patch('infrastructure.services.event_publisher.pika.BlockingConnection')
    def test_publish_user_registered_event_success(self, mock_connection):
        mock_channel = Mock()
        mock_connection.return_value.channel.return_value = mock_channel

        result = self.publisher.publish_user_registered({
            'user_id': 1,
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe'
        })

        assert result is True
        mock_channel.basic_publish.assert_called_once()

    @patch('infrastructure.services.event_publisher.pika.BlockingConnection')
    def test_publish_user_registered_event_failure(self, mock_connection):
        mock_connection.side_effect = Exception('RabbitMQ Error')

        result = self.publisher.publish_user_registered({
            'user_id': 1,
            'email': 'test@example.com'
        })

        assert result is False
