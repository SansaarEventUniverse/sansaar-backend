import pytest
from domain.models import PersonalizationRule
from infrastructure.repositories.personalization_repository import PersonalizationRepository

@pytest.mark.django_db
class TestPersonalizationRepository:
    def test_get_analytics(self):
        """Test getting personalization analytics"""
        PersonalizationRule.objects.create(name="Rule 1", rule_type="content", conditions={}, is_active=True)
        PersonalizationRule.objects.create(name="Rule 2", rule_type="email", conditions={}, is_active=False)
        PersonalizationRule.objects.create(name="Rule 3", rule_type="content", conditions={}, is_active=True)
        
        repo = PersonalizationRepository()
        analytics = repo.get_analytics()
        
        assert analytics['total_rules'] == 3
        assert analytics['active'] == 2
        assert analytics['inactive'] == 1
