from django.db.models import Q
from domain.models import Forum

class ForumRepository:
    def get_by_category(self, category):
        return Forum.objects.filter(category=category, is_active=True)
    
    def search(self, query):
        return Forum.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query),
            is_active=True
        )
