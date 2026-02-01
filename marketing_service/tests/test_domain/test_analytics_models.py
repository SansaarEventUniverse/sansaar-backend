import pytest
from domain.models import CampaignAnalytics, PerformanceMetric

@pytest.mark.django_db
class TestCampaignAnalytics:
    def test_create_analytics(self):
        """Test creating campaign analytics"""
        analytics = CampaignAnalytics.objects.create(
            campaign_id=1,
            campaign_type="email",
            total_sent=1000,
            total_delivered=950,
            total_opened=500,
            total_clicked=200
        )
        assert analytics.campaign_id == 1
        assert analytics.total_sent == 1000

    def test_calculate_open_rate(self):
        """Test calculating open rate"""
        analytics = CampaignAnalytics.objects.create(
            campaign_id=1,
            campaign_type="email",
            total_sent=1000,
            total_delivered=950,
            total_opened=500,
            total_clicked=200
        )
        assert round(analytics.calculate_open_rate(), 2) == 52.63

    def test_calculate_click_rate(self):
        """Test calculating click rate"""
        analytics = CampaignAnalytics.objects.create(
            campaign_id=1,
            campaign_type="email",
            total_sent=1000,
            total_delivered=950,
            total_opened=500,
            total_clicked=200
        )
        assert round(analytics.calculate_click_rate(), 2) == 21.05

@pytest.mark.django_db
class TestPerformanceMetric:
    def test_create_metric(self):
        """Test creating performance metric"""
        metric = PerformanceMetric.objects.create(
            campaign_id=1,
            metric_name="conversion_rate",
            metric_value=15.5
        )
        assert metric.metric_name == "conversion_rate"
        assert metric.metric_value == 15.5

    def test_metric_validation(self):
        """Test metric validation"""
        metric = PerformanceMetric.objects.create(
            campaign_id=1,
            metric_name="engagement",
            metric_value=75.0
        )
        assert metric.is_valid()
