from domain.models import AudienceSegment, SegmentRule

class SegmentationService:
    def create_segment(self, data):
        return AudienceSegment.objects.create(**data)

    def get_segments(self):
        return AudienceSegment.objects.all()

    def get_segment(self, segment_id):
        return AudienceSegment.objects.get(id=segment_id)

class AudienceAnalysisService:
    def analyze_audience(self, segment_id):
        segment = AudienceSegment.objects.get(id=segment_id)
        return {'segment_id': segment_id, 'status': segment.status}

class TargetingService:
    def create_rule(self, segment_id, data):
        segment = AudienceSegment.objects.get(id=segment_id)
        return SegmentRule.objects.create(segment=segment, **data)

    def get_rules(self, segment_id):
        return SegmentRule.objects.filter(segment_id=segment_id)
