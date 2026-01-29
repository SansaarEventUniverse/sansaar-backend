from domain.models import SocialMediaPost

class SocialMediaRepository:
    def get_analytics(self):
        total = SocialMediaPost.objects.count()
        published = SocialMediaPost.objects.filter(status='published').count()
        failed = SocialMediaPost.objects.filter(status='failed').count()
        
        return {
            'total_posts': total,
            'published': published,
            'failed': failed
        }
