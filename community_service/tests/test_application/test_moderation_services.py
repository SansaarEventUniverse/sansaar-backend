import pytest
from domain.models import ModerationRule, ModerationAction
from application.services.moderation_service import ModerationService, SafetyMonitoringService, AutoModerationService

@pytest.mark.django_db
class TestModerationService:
    def test_create_rule(self):
        service = ModerationService()
        rule = service.create_rule({
            'name': 'Spam Filter',
            'rule_type': 'spam',
            'pattern': 'spam|scam',
            'severity': 'high'
        })
        assert rule.name == 'Spam Filter'
    
    def test_get_active_rules(self):
        ModerationRule.objects.create(name='Active', rule_type='spam', pattern='test', severity='low', is_active=True)
        ModerationRule.objects.create(name='Inactive', rule_type='spam', pattern='test', severity='low', is_active=False)
        service = ModerationService()
        rules = service.get_active_rules()
        assert rules.count() == 1
    
    def test_check_content_violation(self):
        ModerationRule.objects.create(name='Spam', rule_type='spam', pattern='spam|scam', severity='high')
        service = ModerationService()
        violations = service.check_content('This is a spam message')
        assert len(violations) == 1
    
    def test_check_content_no_violation(self):
        ModerationRule.objects.create(name='Spam', rule_type='spam', pattern='spam|scam', severity='high')
        service = ModerationService()
        violations = service.check_content('This is a normal message')
        assert len(violations) == 0

@pytest.mark.django_db
class TestSafetyMonitoringService:
    def test_create_action(self):
        service = SafetyMonitoringService()
        action = service.create_action({
            'action_type': 'warning',
            'target_type': 'post',
            'target_id': 1,
            'reason': 'Test'
        })
        assert action.status == 'pending'
    
    def test_get_pending_actions(self):
        ModerationAction.objects.create(action_type='warning', target_type='post', target_id=1, reason='Test', status='pending')
        ModerationAction.objects.create(action_type='remove', target_type='post', target_id=2, reason='Test', status='approved')
        service = SafetyMonitoringService()
        pending = service.get_pending_actions()
        assert pending.count() == 1
    
    def test_approve_action(self):
        action = ModerationAction.objects.create(action_type='warning', target_type='post', target_id=1, reason='Test')
        service = SafetyMonitoringService()
        updated = service.approve_action(action.id)
        assert updated.status == 'approved'

@pytest.mark.django_db
class TestAutoModerationService:
    def test_auto_moderate_with_violation(self):
        ModerationRule.objects.create(name='Spam', rule_type='spam', pattern='spam', severity='high')
        service = AutoModerationService()
        actions = service.auto_moderate('This is spam', 'post', 1)
        assert len(actions) == 1
        assert actions[0].action_type == 'remove'
    
    def test_auto_moderate_no_violation(self):
        ModerationRule.objects.create(name='Spam', rule_type='spam', pattern='spam', severity='high')
        service = AutoModerationService()
        actions = service.auto_moderate('This is clean', 'post', 1)
        assert len(actions) == 0
