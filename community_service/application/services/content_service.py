from domain.models import SharedContent, ContentCollaboration

class ContentSharingService:
    def create_content(self, data):
        return SharedContent.objects.create(**data)
    
    def get_published_content(self):
        return SharedContent.objects.filter(status='published')
    
    def get_user_content(self, user_id):
        return SharedContent.objects.filter(creator_user_id=user_id)

class CollaborationService:
    def add_collaborator(self, content_id, user_id, role='viewer'):
        content = SharedContent.objects.get(id=content_id)
        return ContentCollaboration.objects.create(
            content=content,
            user_id=user_id,
            role=role
        )
    
    def get_collaborators(self, content_id):
        return ContentCollaboration.objects.filter(content_id=content_id)
    
    def get_user_collaborations(self, user_id):
        return ContentCollaboration.objects.filter(user_id=user_id)

class ContentModerationService:
    def publish_content(self, content_id):
        content = SharedContent.objects.get(id=content_id)
        content.publish()
        return content
    
    def archive_content(self, content_id):
        content = SharedContent.objects.get(id=content_id)
        content.archive()
        return content
