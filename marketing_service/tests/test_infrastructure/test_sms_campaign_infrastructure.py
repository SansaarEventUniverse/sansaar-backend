import pytest
from domain.models import SMSCampaign
from infrastructure.repositories.sms_campaign_repository import SMSCampaignRepository

@pytest.mark.django_db
class TestSMSCampaignRepository:
    def test_get_analytics(self):
        """Test getting SMS campaign analytics"""
        SMSCampaign.objects.create(name="Campaign 1", message="Test", status='sent')
        SMSCampaign.objects.create(name="Campaign 2", message="Test", status='failed')
        SMSCampaign.objects.create(name="Campaign 3", message="Test", status='draft')
        
        repo = SMSCampaignRepository()
        analytics = repo.get_analytics()
        
        assert analytics['total_campaigns'] == 3
        assert analytics['sent'] == 1
        assert analytics['failed'] == 1
