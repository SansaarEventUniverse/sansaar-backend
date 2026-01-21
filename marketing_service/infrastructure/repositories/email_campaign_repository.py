from domain.models import EmailCampaign
from django.db.models import Count

class EmailCampaignRepository:
    def get_campaign_analytics(self):
        total = EmailCampaign.objects.count()
        sent = EmailCampaign.objects.filter(status='sent').count()
        
        return {
            'total_campaigns': total,
            'sent_campaigns': sent,
            'draft_campaigns': EmailCampaign.objects.filter(status='draft').count(),
            'scheduled_campaigns': EmailCampaign.objects.filter(status='scheduled').count()
        }

    def get_campaigns_by_status(self, status):
        return EmailCampaign.objects.filter(status=status)
