from domain.models import CustomerJourney, JourneyStage

class JourneyRepository:
    def get_journey_stats(self):
        total_journeys = CustomerJourney.objects.count()
        total_stages = JourneyStage.objects.count()
        return {'total_journeys': total_journeys, 'total_stages': total_stages}
