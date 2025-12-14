from domain.models import FinancialReport


class FinancialRepository:
    def save_report(self, event_id: str, total_revenue, total_expenses):
        report, _ = FinancialReport.objects.update_or_create(
            event_id=event_id,
            defaults={'total_revenue': total_revenue, 'total_expenses': total_expenses}
        )
        return report

    def get_report(self, event_id: str):
        return FinancialReport.objects.get(event_id=event_id)
