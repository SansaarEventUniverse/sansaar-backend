import pytest
from rest_framework.test import APIClient
from domain.models import SMSCampaign

@pytest.mark.django_db
class TestSMSCampaignAPI:
    def test_create_campaign(self):
        """Test creating SMS campaign via API"""
        client = APIClient()
        response = client.post('/api/marketing/sms-campaigns/', {
            'name': 'Test SMS',
            'message': 'Test Message'
        }, format='json')
        
        assert response.status_code == 201
        assert response.data['name'] == 'Test SMS'

    def test_list_campaigns(self):
        """Test listing SMS campaigns"""
        SMSCampaign.objects.create(name="Campaign 1", message="Message 1")
        
        client = APIClient()
        response = client.get('/api/marketing/sms-campaigns/')
        
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_send_campaign(self):
        """Test sending SMS campaign"""
        campaign = SMSCampaign.objects.create(
            name="Test",
            message="Hello",
            status='scheduled'
        )
        
        client = APIClient()
        response = client.post(f'/api/marketing/sms-campaigns/{campaign.id}/send/', {
            'phone_numbers': ['+1234567890']
        }, format='json')
        
        assert response.status_code == 200
        campaign.refresh_from_db()
        assert campaign.status in ['sent', 'failed']
