import tweepy
from django.conf import settings

class TwitterService:
    def __init__(self):
        try:
            auth = tweepy.OAuthHandler(settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET)
            auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)
            self.api = tweepy.API(auth)
        except Exception:
            self.api = None

    def post_tweet(self, message):
        if not self.api:
            raise Exception("Twitter not configured")
        
        try:
            result = self.api.update_status(message)
            return {'id': result.id_str}
        except Exception as e:
            raise Exception(f"Twitter post failed: {str(e)}")
