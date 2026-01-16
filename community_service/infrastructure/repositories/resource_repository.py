from domain.models import ResourceLibrary, SharedResource
from django.db.models import Count, Sum

class ResourceRepository:
    def get_library_stats(self, library_id):
        library = ResourceLibrary.objects.get(id=library_id)
        resources = SharedResource.objects.filter(library=library)
        
        return {
            'total_resources': resources.count(),
            'total_downloads': resources.aggregate(Sum('download_count'))['download_count__sum'] or 0,
            'file_types': list(resources.values_list('file_type', flat=True).distinct())
        }

    def get_popular_resources(self, limit=10):
        return SharedResource.objects.order_by('-download_count')[:limit]

    def get_recent_resources(self, limit=10):
        return SharedResource.objects.order_by('-created_at')[:limit]
