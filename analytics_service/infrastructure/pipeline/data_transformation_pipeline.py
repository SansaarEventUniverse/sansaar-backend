class DataTransformationPipeline:
    def process(self, data: list, chart_type: str):
        if chart_type == "bar":
            return {"values": [item.get("y", 0) for item in data]}
        return {"data": data}
