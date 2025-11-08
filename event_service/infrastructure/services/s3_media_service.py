import uuid
import boto3
from django.conf import settings


class S3MediaService:
    """Service for S3 media storage."""
    
    def __init__(self):
        s3_config = {
            'aws_access_key_id': settings.AWS_ACCESS_KEY_ID,
            'aws_secret_access_key': settings.AWS_SECRET_ACCESS_KEY,
            'region_name': settings.AWS_REGION,
        }
        
        if settings.AWS_S3_ENDPOINT_URL:
            s3_config['endpoint_url'] = settings.AWS_S3_ENDPOINT_URL
        
        self.s3_client = boto3.client('s3', **s3_config)
        self.bucket_name = settings.AWS_S3_BUCKET_NAME
    
    def generate_upload_url(self, event_id: uuid.UUID, file_name: str, 
                           content_type: str) -> dict:
        """Generate presigned URL for upload."""
        key = f"events/{event_id}/media/{uuid.uuid4()}_{file_name}"
        
        url = self.s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': self.bucket_name,
                'Key': key,
                'ContentType': content_type,
            },
            ExpiresIn=3600  # 1 hour
        )
        
        return {
            'upload_url': url,
            's3_key': key,
            'cdn_url': self._get_cdn_url(key),
        }
    
    def delete_file(self, s3_key: str) -> None:
        """Delete file from S3."""
        self.s3_client.delete_object(
            Bucket=self.bucket_name,
            Key=s3_key
        )
    
    def _get_cdn_url(self, s3_key: str) -> str:
        """Get CDN URL for file."""
        if settings.AWS_S3_CUSTOM_DOMAIN:
            return f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{s3_key}"
        return f"https://{self.bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/{s3_key}"
