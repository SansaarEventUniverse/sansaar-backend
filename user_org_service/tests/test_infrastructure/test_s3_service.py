from io import BytesIO
from unittest.mock import Mock, patch

from infrastructure.storage.s3_service import S3Service


class TestS3Service:
    @patch('infrastructure.storage.s3_service.boto3')
    def test_upload_profile_picture(self, mock_boto3):
        mock_s3_client = Mock()
        mock_boto3.client.return_value = mock_s3_client

        service = S3Service()
        
        file = BytesIO(b'test content')
        file.name = 'profile.jpg'
        
        url = service.upload_profile_picture(file, 'user123')
        
        assert 'user123' in url
        assert 'profile.jpg' in url
        mock_s3_client.upload_fileobj.assert_called_once()

    @patch('infrastructure.storage.s3_service.boto3')
    def test_delete_profile_picture(self, mock_boto3):
        mock_s3_client = Mock()
        mock_boto3.client.return_value = mock_s3_client

        service = S3Service()
        service.delete_profile_picture('profile-pictures/user123/profile.jpg')
        
        mock_s3_client.delete_object.assert_called_once()

    @patch('infrastructure.storage.s3_service.boto3')
    def test_check_connection_success(self, mock_boto3):
        mock_s3_client = Mock()
        mock_boto3.client.return_value = mock_s3_client

        service = S3Service()
        result = service.check_connection()
        
        assert result is True
        mock_s3_client.head_bucket.assert_called_once()

    @patch('infrastructure.storage.s3_service.boto3')
    def test_check_connection_failure(self, mock_boto3):
        mock_s3_client = Mock()
        mock_s3_client.head_bucket.side_effect = Exception('Connection failed')
        mock_boto3.client.return_value = mock_s3_client

        service = S3Service()
        result = service.check_connection()
        
        assert result is False
