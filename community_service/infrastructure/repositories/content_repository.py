from domain.models import SharedContent, ContentCollaboration
from django.db.models import Count

class ContentRepository:
    def get_trending_content(self, limit=10):
        return SharedContent.objects.filter(
            status='published'
        ).annotate(
            collab_count=Count('collaborations')
        ).order_by('-collab_count', '-created_at')[:limit]
    
    def get_content_stats(self, content_id):
        content = SharedContent.objects.get(id=content_id)
        collaborators = ContentCollaboration.objects.filter(content_id=content_id).count()
        editors = ContentCollaboration.objects.filter(content_id=content_id, role__in=['editor', 'owner']).count()
        
        return {
            'title': content.title,
            'status': content.status,
            'collaborators': collaborators,
            'editors': editors,
            'is_collaborative': content.is_collaborative
        }
