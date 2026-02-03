from domain.models import MarketingIntelligence

class IntelligenceRepository:
    def get_stats(self):
        total = MarketingIntelligence.objects.count()
        return {'total_intelligence_records': total}
