from domain.models import Chart


class ChartRenderer:
    def render(self, chart_id: int):
        chart = Chart.objects.get(id=chart_id)
        return {
            "chart_type": chart.chart_type,
            "data": chart.data,
            "config": chart.config
        }
