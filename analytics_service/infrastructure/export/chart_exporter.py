from domain.models import Chart


class ChartExporter:
    def export(self, chart_id: int, format: str):
        chart = Chart.objects.get(id=chart_id)
        return {
            "chart_type": chart.chart_type,
            "data": chart.data,
            "config": chart.config
        }
