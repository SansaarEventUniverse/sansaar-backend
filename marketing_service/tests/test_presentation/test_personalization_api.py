import pytest
from rest_framework.test import APIClient
from domain.models import PersonalizationRule, UserPreference

@pytest.mark.django_db
class TestPersonalizationAPI:
    def test_personalize_content(self):
        """Test personalizing content via API"""
        client = APIClient()
        response = client.post('/api/marketing/personalization/content/', {
            'user_id': 123,
            'content': {'message': 'Test'}
        }, format='json')
        
        assert response.status_code == 200
        assert response.data['customized'] is True

    def test_update_preferences(self):
        """Test updating user preferences"""
        client = APIClient()
        response = client.put('/api/marketing/users/123/preferences/', {
            'preference_type': 'interests',
            'preference_data': {'categories': ['music']}
        }, format='json')
        
        assert response.status_code == 200

    def test_get_personalization(self):
        """Test getting personalization rules"""
        PersonalizationRule.objects.create(name="Rule 1", rule_type="content", conditions={})
        
        client = APIClient()
        response = client.get('/api/marketing/personalization/')
        
        assert response.status_code == 200
        assert len(response.data) == 1
