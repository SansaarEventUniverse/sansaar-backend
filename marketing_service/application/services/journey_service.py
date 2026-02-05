from domain.models import CustomerJourney, JourneyStage

class CustomerJourneyService:
    def create_journey(self, user_id, campaign_id, journey_data):
        return CustomerJourney.objects.create(
            user_id=user_id,
            campaign_id=campaign_id,
            journey_data=journey_data
        )

class JourneyMappingService:
    def map_journey(self, journey_id, stages):
        mapped_stages = []
        for i, stage in enumerate(stages, 1):
            journey_stage = JourneyStage.objects.create(
                journey_id=journey_id,
                stage_name=stage['name'],
                stage_order=i,
                stage_data=stage.get('data', {})
            )
            mapped_stages.append(journey_stage.stage_name)
        return {'journey_id': journey_id, 'stages': mapped_stages}

class JourneyAnalysisService:
    def analyze_journey(self, user_id):
        journeys = CustomerJourney.objects.filter(user_id=user_id)
        total_stages = sum(len(j.get_stages()) for j in journeys)
        return {'user_id': user_id, 'total_journeys': journeys.count(), 'total_stages': total_stages}
