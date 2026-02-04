import pytest
from django.core.exceptions import ValidationError
from domain.models import AttributionModel, TouchPoint

@pytest.mark.django_db
class TestAttributionModel:
    def test_create_attribution(self):
        attribution = AttributionModel.objects.create(
            campaign_id=1,
            model_type='last_click',
            conversion_value=100.0,
            attribution_data={'channel': 'email', 'weight': 1.0}
        )
        assert attribution.campaign_id == 1
        assert attribution.model_type == 'last_click'
        assert attribution.conversion_value == 100.0

    def test_calculate_attribution(self):
        attribution = AttributionModel.objects.create(
            campaign_id=1,
            model_type='linear',
            conversion_value=100.0,
            attribution_data={'touchpoints': 4}
        )
        result = attribution.calculate_attribution()
        assert result['per_touchpoint'] == 25.0

    def test_get_attribution_weights(self):
        attribution = AttributionModel.objects.create(
            campaign_id=1,
            model_type='time_decay',
            conversion_value=100.0,
            attribution_data={'channels': ['email', 'social', 'search']}
        )
        weights = attribution.get_attribution_weights()
        assert 'email' in weights
        assert round(sum(weights.values()), 2) == 0.99

@pytest.mark.django_db
class TestTouchPoint:
    def test_create_touchpoint(self):
        touchpoint = TouchPoint.objects.create(
            campaign_id=1,
            channel='email',
            user_id=123,
            touchpoint_data={'action': 'click', 'timestamp': '2024-01-01'}
        )
        assert touchpoint.channel == 'email'
        assert touchpoint.user_id == 123

    def test_touchpoint_validation(self):
        touchpoint = TouchPoint(
            campaign_id=1,
            channel='',
            user_id=123,
            touchpoint_data={}
        )
        with pytest.raises(ValidationError):
            touchpoint.full_clean()

    def test_get_touchpoint_value(self):
        touchpoint = TouchPoint.objects.create(
            campaign_id=1,
            channel='search',
            user_id=123,
            touchpoint_data={'value': 50.0}
        )
        value = touchpoint.get_value()
        assert value == 50.0
