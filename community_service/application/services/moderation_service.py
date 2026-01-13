import re
from domain.models import ModerationRule, ModerationAction

class ModerationService:
    def create_rule(self, data):
        return ModerationRule.objects.create(**data)
    
    def get_active_rules(self):
        return ModerationRule.objects.filter(is_active=True)
    
    def check_content(self, content):
        """Check content against active moderation rules"""
        violations = []
        rules = self.get_active_rules()
        
        for rule in rules:
            if re.search(rule.pattern, content, re.IGNORECASE):
                violations.append(rule)
        
        return violations

class SafetyMonitoringService:
    def create_action(self, data):
        return ModerationAction.objects.create(**data)
    
    def get_pending_actions(self):
        return ModerationAction.objects.filter(status='pending')
    
    def approve_action(self, action_id):
        action = ModerationAction.objects.get(id=action_id)
        action.approve()
        return action

class AutoModerationService:
    def auto_moderate(self, content, target_type, target_id):
        """Automatically moderate content based on rules"""
        moderation_service = ModerationService()
        violations = moderation_service.check_content(content)
        
        actions = []
        for rule in violations:
            action = ModerationAction.objects.create(
                rule=rule,
                action_type='warning' if rule.severity == 'low' else 'remove',
                target_type=target_type,
                target_id=target_id,
                reason=f'Violated rule: {rule.name}',
                status='approved' if rule.severity == 'high' else 'pending'
            )
            actions.append(action)
        
        return actions
