from domain.models import Chart, Visualization


class ChartGenerationService:
    def generate_chart(self, visualization_id: int, chart_type: str, data: dict, config: dict = None):
        visualization = Visualization.objects.get(id=visualization_id)
        return Chart.objects.create(
            visualization=visualization,
            chart_type=chart_type,
            data=data,
            config=config or {}
        )

    def get_chart_data(self, chart_id: int):
        chart = Chart.objects.get(id=chart_id)
        return chart.data
