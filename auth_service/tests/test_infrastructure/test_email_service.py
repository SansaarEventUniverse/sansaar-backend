from unittest.mock import Mock, patch

from infrastructure.services.email_service import EmailService


class TestEmailService:
    @patch('infrastructure.services.email_service.SendGridAPIClient')
    def test_send_verification_email_success(self, mock_sendgrid):
        mock_client = Mock()
        mock_sendgrid.return_value = mock_client
        mock_response = Mock()
        mock_response.status_code = 202
        mock_client.send.return_value = mock_response

        service = EmailService()
        result = service.send_verification_email(
            to_email='test@example.com',
            verification_token='abc123',
            first_name='John'
        )

        assert result is True
        mock_client.send.assert_called_once()

    @patch('infrastructure.services.email_service.SendGridAPIClient')
    def test_send_verification_email_failure(self, mock_sendgrid):
        mock_client = Mock()
        mock_sendgrid.return_value = mock_client
        mock_client.send.side_effect = Exception('SendGrid Error')

        service = EmailService()
        result = service.send_verification_email(
            to_email='test@example.com',
            verification_token='abc123',
            first_name='John'
        )

        assert result is False
