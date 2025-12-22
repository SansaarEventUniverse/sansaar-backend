from domain.models import AuditTrail


class AuditReportingService:
    def generate_audit_report(self, user_id: str):
        trails = AuditTrail.objects.filter(user_id=user_id)
        return {
            "user_id": user_id,
            "total_actions": trails.count(),
            "actions": list(trails.values('action', 'resource', 'status', 'created_at'))
        }

    def search_audit_trail(self, criteria: dict):
        queryset = AuditTrail.objects.all()
        if 'action' in criteria:
            queryset = queryset.filter(action=criteria['action'])
        if 'user_id' in criteria:
            queryset = queryset.filter(user_id=criteria['user_id'])
        return list(queryset)
