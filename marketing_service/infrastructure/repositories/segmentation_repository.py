from domain.models import AudienceSegment

class SegmentationRepository:
    def get_analytics(self):
        total = AudienceSegment.objects.count()
        active = AudienceSegment.objects.filter(status='active').count()
        archived = AudienceSegment.objects.filter(status='archived').count()
        
        return {
            'total_segments': total,
            'active': active,
            'archived': archived
        }
