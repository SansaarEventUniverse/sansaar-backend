import boto3
from django.conf import settings


class S3Service:
    def __init__(self):
        config = {
            'aws_access_key_id': settings.AWS_ACCESS_KEY_ID,
            'aws_secret_access_key': settings.AWS_SECRET_ACCESS_KEY,
            'region_name': settings.AWS_S3_REGION_NAME
        }
        
        # Add endpoint_url for MinIO
        if settings.AWS_S3_ENDPOINT_URL:
            config['endpoint_url'] = settings.AWS_S3_ENDPOINT_URL
            
        self.s3_client = boto3.client('s3', **config)
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    def upload_profile_picture(self, file, user_id):
        key = f'{settings.AWS_LOCATION}/{user_id}/{file.name}'
        self.s3_client.upload_fileobj(file, self.bucket_name, key)
        
        if settings.AWS_S3_ENDPOINT_URL:
            return f'{settings.AWS_S3_ENDPOINT_URL}/{self.bucket_name}/{key}'
        return f'https://{self.bucket_name}.s3.amazonaws.com/{key}'

    def delete_profile_picture(self, key):
        self.s3_client.delete_object(Bucket=self.bucket_name, Key=key)

    def check_connection(self):
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            return True
        except Exception:
            return False
