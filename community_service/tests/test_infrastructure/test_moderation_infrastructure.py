import pytest
from domain.models import ModerationRule, ModerationAction
from infrastructure.repositories.moderation_repository import ModerationRepository

@pytest.mark.django_db
class TestModerationRepository:
    def test_get_moderation_stats(self):
        ModerationAction.objects.create(action_type='warning', target_type='post', target_id=1, reason='Test', status='pending')
        ModerationAction.objects.create(action_type='remove', target_type='post', target_id=2, reason='Test', status='approved')
        ModerationAction.objects.create(action_type='suspend', target_type='user', target_id=3, reason='Test', status='rejected')
        
        repo = ModerationRepository()
        stats = repo.get_moderation_stats()
        assert stats['total_actions'] == 3
        assert stats['pending'] == 1
        assert stats['approved'] == 1
        assert stats['rejected'] == 1
    
    def test_get_rule_effectiveness(self):
        rule = ModerationRule.objects.create(name='Test', rule_type='spam', pattern='test', severity='high')
        ModerationAction.objects.create(rule=rule, action_type='warning', target_type='post', target_id=1, reason='Test', status='approved')
        ModerationAction.objects.create(rule=rule, action_type='remove', target_type='post', target_id=2, reason='Test', status='approved')
        ModerationAction.objects.create(rule=rule, action_type='warning', target_type='post', target_id=3, reason='Test', status='rejected')
        
        repo = ModerationRepository()
        effectiveness = repo.get_rule_effectiveness(rule.id)
        assert effectiveness['total_actions'] == 3
        assert effectiveness['approved_actions'] == 2
        assert effectiveness['effectiveness'] == pytest.approx(66.67, 0.1)
