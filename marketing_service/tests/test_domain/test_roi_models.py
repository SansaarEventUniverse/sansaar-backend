import pytest
from domain.models import ROIAnalytics, ROIMetric

@pytest.mark.django_db
class TestROIAnalytics:
    def test_create_roi_analytics(self):
        roi = ROIAnalytics.objects.create(
            campaign_id=1,
            revenue=10000.0,
            cost=2000.0,
            roi_data={'period': 'Q1'}
        )
        assert roi.campaign_id == 1
        assert roi.revenue == 10000.0
        assert roi.cost == 2000.0

    def test_calculate_roi(self):
        roi = ROIAnalytics.objects.create(
            campaign_id=1,
            revenue=10000.0,
            cost=2000.0,
            roi_data={}
        )
        result = roi.calculate_roi()
        assert result == 400.0

    def test_get_profit(self):
        roi = ROIAnalytics.objects.create(
            campaign_id=1,
            revenue=10000.0,
            cost=2000.0,
            roi_data={}
        )
        profit = roi.get_profit()
        assert profit == 8000.0

@pytest.mark.django_db
class TestROIMetric:
    def test_create_metric(self):
        metric = ROIMetric.objects.create(
            analytics_id=1,
            metric_name='conversion_rate',
            metric_value=5.5,
            metric_data={'target': 6.0}
        )
        assert metric.metric_name == 'conversion_rate'
        assert metric.metric_value == 5.5

    def test_is_target_met(self):
        metric = ROIMetric.objects.create(
            analytics_id=1,
            metric_name='conversion_rate',
            metric_value=6.5,
            metric_data={'target': 6.0}
        )
        assert metric.is_target_met() is True

    def test_get_variance(self):
        metric = ROIMetric.objects.create(
            analytics_id=1,
            metric_name='ctr',
            metric_value=3.0,
            metric_data={'target': 2.5}
        )
        variance = metric.get_variance()
        assert variance == 20.0
