from domain.models import Forum

class ForumService:
    def create(self, data):
        return Forum.objects.create(**data)
    
    def get_active_forums(self):
        return Forum.objects.filter(is_active=True)
