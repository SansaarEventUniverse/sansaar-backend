class DataTransformationService:
    def transform_data(self, raw_data: list, chart_type: str):
        if chart_type == "bar":
            return {"values": [item.get("y", 0) for item in raw_data]}
        return {"data": raw_data}

    def aggregate_data(self, data: list, operation: str):
        if operation == "sum":
            return sum(data)
        elif operation == "avg":
            return sum(data) / len(data) if data else 0
        return 0
