from django.conf import settings
from elasticsearch import Elasticsearch


class AuditLogSearchService:
    def __init__(self):
        self.es = Elasticsearch([f"http://{settings.ELASTICSEARCH_HOST}:{settings.ELASTICSEARCH_PORT}"])
        self.index = "superadmin_audit_logs"

    def search(
        self,
        start_date: str = None,
        end_date: str = None,
        event_type: str = None,
        admin_id: str = None,
        page: int = 1,
        limit: int = 50,
    ) -> dict:
        query = {"bool": {"must": []}}

        if start_date or end_date:
            date_range = {}
            if start_date:
                date_range["gte"] = start_date
            if end_date:
                date_range["lte"] = end_date
            query["bool"]["must"].append({"range": {"timestamp": date_range}})

        if event_type:
            query["bool"]["must"].append({"term": {"event_type.keyword": event_type}})

        if admin_id:
            query["bool"]["must"].append({"term": {"admin_id.keyword": admin_id}})

        if not query["bool"]["must"]:
            query = {"match_all": {}}

        from_offset = (page - 1) * limit

        try:
            response = self.es.search(
                index=self.index,
                body={"query": query, "from": from_offset, "size": limit, "sort": [{"timestamp": "desc"}]},
            )

            logs = [hit["_source"] for hit in response["hits"]["hits"]]
            total = response["hits"]["total"]["value"]

            return {"logs": logs, "total": total, "page": page, "limit": limit}
        except Exception:
            return {"logs": [], "total": 0, "page": page, "limit": limit}
