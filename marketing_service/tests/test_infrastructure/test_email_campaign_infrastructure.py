import pytest
from unittest.mock import Mock, patch
from domain.models import EmailCampaign, EmailTemplate
from infrastructure.repositories.email_campaign_repository import EmailCampaignRepository

@pytest.mark.django_db
class TestEmailCampaignRepository:
    def test_get_campaign_analytics(self):
        """Test getting campaign analytics"""
        EmailCampaign.objects.create(name="Campaign 1", subject="Subject 1", status='sent')
        EmailCampaign.objects.create(name="Campaign 2", subject="Subject 2", status='draft')
        
        repo = EmailCampaignRepository()
        analytics = repo.get_campaign_analytics()
        
        assert analytics['total_campaigns'] == 2
        assert analytics['sent_campaigns'] == 1

    def test_get_campaigns_by_status(self):
        """Test getting campaigns by status"""
        EmailCampaign.objects.create(name="Campaign 1", subject="Subject 1", status='sent')
        EmailCampaign.objects.create(name="Campaign 2", subject="Subject 2", status='sent')
        EmailCampaign.objects.create(name="Campaign 3", subject="Subject 3", status='draft')
        
        repo = EmailCampaignRepository()
        sent_campaigns = repo.get_campaigns_by_status('sent')
        
        assert sent_campaigns.count() == 2
