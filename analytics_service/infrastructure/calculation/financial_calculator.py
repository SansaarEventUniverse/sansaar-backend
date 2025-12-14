from domain.models import FinancialReport


class FinancialCalculator:
    def calculate_metrics(self, event_id: str):
        report = FinancialReport.objects.get(event_id=event_id)
        return {
            'net_profit': report.net_profit,
            'profit_margin': report.calculate_profit_margin()
        }
