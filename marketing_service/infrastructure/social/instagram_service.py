from instagrapi import Client
from django.conf import settings

class InstagramService:
    def __init__(self):
        try:
            self.client = Client()
            self.client.login(settings.INSTAGRAM_USERNAME, settings.INSTAGRAM_PASSWORD)
        except Exception:
            self.client = None

    def post_photo(self, image_path, caption):
        if not self.client:
            raise Exception("Instagram not configured")
        
        try:
            result = self.client.photo_upload(image_path, caption)
            return {'id': result.pk}
        except Exception as e:
            raise Exception(f"Instagram post failed: {str(e)}")
