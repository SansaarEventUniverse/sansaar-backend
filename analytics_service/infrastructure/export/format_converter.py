import json


class FormatConverter:
    def convert(self, data: dict, format: str):
        if format == "csv":
            return self._to_csv(data)
        elif format == "json":
            return json.dumps(data)
        elif format == "excel":
            return "excel_data"
        elif format == "pdf":
            return "pdf_data"
        return str(data)

    def _to_csv(self, data: dict):
        if "data" in data:
            return ",".join(map(str, data["data"]))
        return str(data)
