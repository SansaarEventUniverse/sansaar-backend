import facebook
from django.conf import settings

class FacebookService:
    def __init__(self):
        try:
            self.graph = facebook.GraphAPI(access_token=settings.FACEBOOK_PAGE_ACCESS_TOKEN)
        except Exception:
            self.graph = None

    def post_to_page(self, message):
        if not self.graph:
            raise Exception("Facebook not configured")
        
        try:
            result = self.graph.put_object(
                parent_object=settings.FACEBOOK_PAGE_ID,
                connection_name="feed",
                message=message
            )
            return result
        except Exception as e:
            raise Exception(f"Facebook post failed: {str(e)}")
