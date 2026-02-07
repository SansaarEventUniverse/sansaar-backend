from domain.models import ROIAnalytics, ROIMetric

class ROIRepository:
    def get_roi_stats(self):
        total_analytics = ROIAnalytics.objects.count()
        total_metrics = ROIMetric.objects.count()
        return {'total_analytics': total_analytics, 'total_metrics': total_metrics}
