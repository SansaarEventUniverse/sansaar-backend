from domain.models import Visualization


class VisualizationService:
    def create_visualization(self, name: str, visualization_type: str, config: dict = None):
        return Visualization.objects.create(
            name=name,
            visualization_type=visualization_type,
            config=config or {}
        )

    def get_visualization(self, visualization_id: int):
        return Visualization.objects.get(id=visualization_id)
