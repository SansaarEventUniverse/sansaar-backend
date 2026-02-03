import pytest
from domain.models import MarketingIntelligence, IntelligenceInsight

@pytest.mark.django_db
class TestMarketingIntelligence:
    def test_create_intelligence(self):
        """Test creating marketing intelligence"""
        intelligence = MarketingIntelligence.objects.create(
            campaign_id=1,
            intelligence_type="performance",
            data={"metric": "conversion_rate", "value": 15.5}
        )
        assert intelligence.campaign_id == 1
        assert intelligence.intelligence_type == "performance"

    def test_generate_insights(self):
        """Test generating insights"""
        intelligence = MarketingIntelligence.objects.create(
            campaign_id=1,
            intelligence_type="performance",
            data={"metric": "conversion_rate", "value": 15.5}
        )
        insights = intelligence.generate_insights()
        assert insights is not None

@pytest.mark.django_db
class TestIntelligenceInsight:
    def test_create_insight(self):
        """Test creating intelligence insight"""
        insight = IntelligenceInsight.objects.create(
            campaign_id=1,
            insight_type="recommendation",
            insight_data={"action": "increase_budget", "confidence": 0.85}
        )
        assert insight.insight_type == "recommendation"
        assert insight.insight_data["confidence"] == 0.85

    def test_insight_validation(self):
        """Test insight validation"""
        insight = IntelligenceInsight.objects.create(
            campaign_id=1,
            insight_type="prediction",
            insight_data={"forecast": "positive"}
        )
        assert insight.is_valid()
