from domain.models import SocialMediaPost, SocialPlatform

class SocialMediaService:
    def create_post(self, data):
        return SocialMediaPost.objects.create(**data)

    def get_posts(self):
        return SocialMediaPost.objects.all()

    def get_post(self, post_id):
        return SocialMediaPost.objects.get(id=post_id)
    
    def publish_post(self, post_id):
        from infrastructure.social.facebook_service import FacebookService
        from infrastructure.social.twitter_service import TwitterService
        
        post = SocialMediaPost.objects.get(id=post_id)
        
        try:
            if post.platform == 'facebook':
                service = FacebookService()
                service.post_to_page(post.content)
            elif post.platform == 'twitter':
                service = TwitterService()
                service.post_tweet(post.content)
            
            post.publish()
            return True
        except Exception as e:
            post.mark_failed()
            return False

class PlatformIntegrationService:
    def connect_platform(self, data):
        return SocialPlatform.objects.create(**data)

    def get_platforms(self):
        return SocialPlatform.objects.filter(is_active=True)

class ContentSchedulingService:
    def schedule_post(self, post_id, scheduled_time):
        post = SocialMediaPost.objects.get(id=post_id)
        post.scheduled_at = scheduled_time
        post.status = 'scheduled'
        post.save()
        return post
