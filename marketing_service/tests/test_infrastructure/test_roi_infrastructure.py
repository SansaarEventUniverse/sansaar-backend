import pytest
from infrastructure.repositories.roi_repository import ROIRepository
from domain.models import ROIAnalytics, ROIMetric

@pytest.mark.django_db
class TestROIRepository:
    def test_get_roi_stats(self):
        ROIAnalytics.objects.create(campaign_id=1, revenue=10000.0, cost=2000.0, roi_data={})
        ROIMetric.objects.create(analytics_id=1, metric_name='ctr', metric_value=3.0, metric_data={})
        repo = ROIRepository()
        stats = repo.get_roi_stats()
        assert stats['total_analytics'] == 1
        assert stats['total_metrics'] == 1
