import pytest
from rest_framework.test import APIClient
from domain.models import ModerationRule, ModerationAction

@pytest.mark.django_db
class TestModerationAPI:
    def setup_method(self):
        self.client = APIClient()
        
    def test_moderation_dashboard(self):
        """Test getting moderation dashboard"""
        ModerationAction.objects.create(
            action_type='warning',
            target_type='post',
            target_id=1,
            reason='Test',
            status='pending'
        )
        
        response = self.client.get('/api/community/admin/moderation/')
        assert response.status_code == 200
        assert 'stats' in response.data
        assert 'pending_actions' in response.data
        assert response.data['stats']['total_actions'] == 1
        
    def test_report_content(self):
        """Test reporting content"""
        response = self.client.post('/api/community/content/1/report/', {
            'target_type': 'post',
            'reason': 'Spam content'
        }, format='json')
        assert response.status_code == 201
        assert response.data['reason'] == 'Spam content'
        assert response.data['status'] == 'pending'
        
    def test_report_content_missing_reason(self):
        """Test reporting content without reason"""
        response = self.client.post('/api/community/content/1/report/', {
            'target_type': 'post'
        }, format='json')
        assert response.status_code == 400
        
    def test_approve_moderation_action(self):
        """Test approving moderation action"""
        action = ModerationAction.objects.create(
            action_type='warning',
            target_type='post',
            target_id=1,
            reason='Test',
            status='pending'
        )
        
        response = self.client.post('/api/community/moderation/actions/', {
            'action_id': action.id,
            'action': 'approve'
        }, format='json')
        assert response.status_code == 200
        assert response.data['status'] == 'approved'
