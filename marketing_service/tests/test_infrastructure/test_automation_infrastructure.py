import pytest
from domain.models import AutomationWorkflow
from infrastructure.repositories.automation_repository import AutomationRepository

@pytest.mark.django_db
class TestAutomationRepository:
    def test_get_analytics(self):
        """Test getting automation analytics"""
        AutomationWorkflow.objects.create(name="Workflow 1", trigger_type="user_signup", status="active")
        AutomationWorkflow.objects.create(name="Workflow 2", trigger_type="event_created", status="paused")
        AutomationWorkflow.objects.create(name="Workflow 3", trigger_type="user_signup", status="draft")
        
        repo = AutomationRepository()
        analytics = repo.get_analytics()
        
        assert analytics['total_workflows'] == 3
        assert analytics['active'] == 1
        assert analytics['paused'] == 1
