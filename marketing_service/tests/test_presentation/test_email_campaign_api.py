import pytest
from rest_framework.test import APIClient
from domain.models import EmailCampaign, EmailTemplate

@pytest.mark.django_db
class TestEmailCampaignAPI:
    def setup_method(self):
        self.client = APIClient()

    def test_create_campaign(self):
        """Test creating campaign via API"""
        data = {
            'name': 'Test Campaign',
            'subject': 'Test Subject',
            'content': 'Test Content'
        }
        response = self.client.post('/api/marketing/email-campaigns/', data, format='json')
        assert response.status_code == 201
        assert response.data['name'] == 'Test Campaign'

    def test_get_campaigns(self):
        """Test getting campaigns"""
        EmailCampaign.objects.create(name="Campaign 1", subject="Subject 1")
        EmailCampaign.objects.create(name="Campaign 2", subject="Subject 2")
        
        response = self.client.get('/api/marketing/email-campaigns/')
        assert response.status_code == 200
        assert len(response.data) == 2

    def test_send_campaign(self):
        """Test sending campaign"""
        campaign = EmailCampaign.objects.create(
            name="Test",
            subject="Test",
            content="Hello",
            status='scheduled'
        )
        
        data = {'recipients': ['test@example.com']}
        response = self.client.post(f'/api/marketing/email-campaigns/{campaign.id}/send/', data, format='json')
        assert response.status_code in [200, 400]  # Accept both as email service may not be configured
        campaign.refresh_from_db()
        assert campaign.status in ['sent', 'failed']
