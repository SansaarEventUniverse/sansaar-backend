from domain.models import FinancialReport


class ProfitLossService:
    def calculate_profit_loss(self, event_id: str):
        report = FinancialReport.objects.get(event_id=event_id)
        return {
            'event_id': report.event_id,
            'total_revenue': report.total_revenue,
            'total_expenses': report.total_expenses,
            'net_profit': report.net_profit,
            'profit_margin': report.calculate_profit_margin()
        }
