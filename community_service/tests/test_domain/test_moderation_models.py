import pytest
from domain.models import ModerationRule, ModerationAction

@pytest.mark.django_db
class TestModerationRule:
    def test_create_moderation_rule(self):
        rule = ModerationRule.objects.create(
            name='Spam Filter',
            rule_type='spam',
            pattern='spam|scam|phishing',
            severity='high'
        )
        assert rule.name == 'Spam Filter'
        assert rule.is_active is True
    
    def test_rule_severity_levels(self):
        low = ModerationRule.objects.create(name='Low', rule_type='keyword', pattern='test', severity='low')
        high = ModerationRule.objects.create(name='High', rule_type='profanity', pattern='bad', severity='high')
        assert low.severity == 'low'
        assert high.severity == 'high'

@pytest.mark.django_db
class TestModerationAction:
    def test_create_moderation_action(self):
        rule = ModerationRule.objects.create(name='Test', rule_type='spam', pattern='test', severity='medium')
        action = ModerationAction.objects.create(
            rule=rule,
            action_type='warning',
            target_type='post',
            target_id=1,
            reason='Spam detected'
        )
        assert action.status == 'pending'
    
    def test_approve_action(self):
        action = ModerationAction.objects.create(
            action_type='remove',
            target_type='comment',
            target_id=2,
            reason='Inappropriate content'
        )
        action.approve()
        assert action.status == 'approved'
    
    def test_reject_action(self):
        action = ModerationAction.objects.create(
            action_type='suspend',
            target_type='user',
            target_id=3,
            reason='False positive'
        )
        action.reject()
        assert action.status == 'rejected'
