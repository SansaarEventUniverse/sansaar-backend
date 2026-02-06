import pytest
from application.services.roi_service import ROIAnalyticsService, ROICalculationService, ROIReportingService
from domain.models import ROIAnalytics

@pytest.mark.django_db
class TestROIAnalyticsService:
    def test_get_roi_analytics(self):
        ROIAnalytics.objects.create(campaign_id=1, revenue=10000.0, cost=2000.0, roi_data={})
        service = ROIAnalyticsService()
        result = service.get_roi_analytics(1)
        assert result.count() == 1

@pytest.mark.django_db
class TestROICalculationService:
    def test_calculate_roi(self):
        service = ROICalculationService()
        result = service.calculate_roi(1, 10000.0, 2000.0)
        assert result['campaign_id'] == 1
        assert result['roi'] == 400.0
        assert result['profit'] == 8000.0

@pytest.mark.django_db
class TestROIReportingService:
    def test_generate_report(self):
        ROIAnalytics.objects.create(campaign_id=1, revenue=10000.0, cost=2000.0, roi_data={})
        service = ROIReportingService()
        result = service.generate_report(1)
        assert result['campaign_id'] == 1
        assert result['roi'] == 400.0
        assert result['profit'] == 8000.0
