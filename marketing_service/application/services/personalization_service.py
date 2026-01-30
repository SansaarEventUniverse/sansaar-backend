from domain.models import PersonalizationRule, UserPreference

class PersonalizationService:
    def create_rule(self, data):
        return PersonalizationRule.objects.create(**data)

    def get_rules(self):
        return PersonalizationRule.objects.filter(is_active=True)

    def get_rule(self, rule_id):
        return PersonalizationRule.objects.get(id=rule_id)

class PreferenceAnalysisService:
    def analyze_user(self, user_id):
        preferences = UserPreference.objects.filter(user_id=user_id)
        return {'user_id': user_id, 'preferences_count': preferences.count()}

    def update_preference(self, user_id, data):
        pref, created = UserPreference.objects.get_or_create(
            user_id=user_id,
            preference_type=data.get('preference_type'),
            defaults={'preference_data': data.get('preference_data', {})}
        )
        if not created:
            pref.preference_data = data.get('preference_data', {})
            pref.save()
        return pref

class ContentCustomizationService:
    def customize_for_user(self, user_id, content_data):
        return {'user_id': user_id, 'customized': True, 'content': content_data}
