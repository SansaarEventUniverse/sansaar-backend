import pytest
from domain.models import PersonalizationRule, UserPreference

@pytest.mark.django_db
class TestPersonalizationRule:
    def test_create_rule(self):
        """Test creating personalization rule"""
        rule = PersonalizationRule.objects.create(
            name="Event Recommendations",
            rule_type="content",
            conditions={"interest": "music"},
            is_active=True
        )
        assert rule.name == "Event Recommendations"
        assert rule.is_active is True

    def test_activate_rule(self):
        """Test activating rule"""
        rule = PersonalizationRule.objects.create(
            name="Test",
            rule_type="content",
            conditions={},
            is_active=False
        )
        rule.activate()
        assert rule.is_active is True

    def test_deactivate_rule(self):
        """Test deactivating rule"""
        rule = PersonalizationRule.objects.create(
            name="Test",
            rule_type="content",
            conditions={},
            is_active=True
        )
        rule.deactivate()
        assert rule.is_active is False

@pytest.mark.django_db
class TestUserPreference:
    def test_create_preference(self):
        """Test creating user preference"""
        pref = UserPreference.objects.create(
            user_id=123,
            preference_type="interests",
            preference_data={"categories": ["music", "sports"]}
        )
        assert pref.user_id == 123
        assert "music" in pref.preference_data["categories"]

    def test_update_preference(self):
        """Test updating preference"""
        pref = UserPreference.objects.create(
            user_id=123,
            preference_type="interests",
            preference_data={"categories": ["music"]}
        )
        pref.preference_data["categories"].append("sports")
        pref.save()
        assert len(pref.preference_data["categories"]) == 2

    def test_preference_validation(self):
        """Test preference validation"""
        pref = UserPreference.objects.create(
            user_id=123,
            preference_type="interests",
            preference_data={}
        )
        assert pref.is_valid()
