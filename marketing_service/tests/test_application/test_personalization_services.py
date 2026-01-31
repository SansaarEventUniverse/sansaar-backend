import pytest
from domain.models import PersonalizationRule, UserPreference
from application.services.personalization_service import PersonalizationService, PreferenceAnalysisService, ContentCustomizationService

@pytest.mark.django_db
class TestPersonalizationService:
    def test_create_rule(self):
        """Test creating personalization rule"""
        service = PersonalizationService()
        rule = service.create_rule({
            'name': 'Event Recommendations',
            'rule_type': 'content',
            'conditions': {}
        })
        assert rule.name == 'Event Recommendations'

    def test_get_rules(self):
        """Test getting rules"""
        PersonalizationRule.objects.create(name="Rule 1", rule_type="content", conditions={})
        PersonalizationRule.objects.create(name="Rule 2", rule_type="email", conditions={})
        
        service = PersonalizationService()
        rules = service.get_rules()
        assert rules.count() == 2

@pytest.mark.django_db
class TestPreferenceAnalysisService:
    def test_analyze_preferences(self):
        """Test analyzing user preferences"""
        UserPreference.objects.create(
            user_id=123,
            preference_type="interests",
            preference_data={"categories": ["music"]}
        )
        
        service = PreferenceAnalysisService()
        result = service.analyze_user(123)
        assert result is not None

@pytest.mark.django_db
class TestContentCustomizationService:
    def test_customize_content(self):
        """Test customizing content"""
        service = ContentCustomizationService()
        result = service.customize_for_user(123, {"content": "Test"})
        assert result is not None
