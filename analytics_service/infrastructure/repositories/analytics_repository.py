from domain.models import AnalyticsEvent


class AnalyticsRepository:
    def save_event(self, event_data):
        return AnalyticsEvent.objects.create(**event_data)

    def get_events_by_type(self, event_type):
        return AnalyticsEvent.objects.filter(event_type=event_type)

    def get_events_by_user(self, user_id):
        return AnalyticsEvent.objects.filter(user_id=user_id)

    def get_unprocessed_events(self):
        return AnalyticsEvent.objects.filter(is_processed=False)
