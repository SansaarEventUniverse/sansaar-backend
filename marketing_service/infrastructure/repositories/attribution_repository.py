from domain.models import AttributionModel, TouchPoint

class AttributionRepository:
    def get_attribution_stats(self):
        total_attributions = AttributionModel.objects.count()
        total_touchpoints = TouchPoint.objects.count()
        return {'total_attributions': total_attributions, 'total_touchpoints': total_touchpoints}
