import pytest
from infrastructure.repositories.attribution_repository import AttributionRepository
from domain.models import AttributionModel, TouchPoint

@pytest.mark.django_db
class TestAttributionRepository:
    def test_get_attribution_stats(self):
        AttributionModel.objects.create(
            campaign_id=1,
            model_type='last_click',
            conversion_value=100.0,
            attribution_data={}
        )
        TouchPoint.objects.create(campaign_id=1, channel='email', user_id=123, touchpoint_data={})
        repo = AttributionRepository()
        stats = repo.get_attribution_stats()
        assert stats['total_attributions'] == 1
        assert stats['total_touchpoints'] == 1
