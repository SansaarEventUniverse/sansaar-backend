from domain.models import SMSCampaign

class SMSCampaignRepository:
    def get_analytics(self):
        total = SMSCampaign.objects.count()
        sent = SMSCampaign.objects.filter(status='sent').count()
        failed = SMSCampaign.objects.filter(status='failed').count()
        
        return {
            'total_campaigns': total,
            'sent': sent,
            'failed': failed
        }
