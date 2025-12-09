from elasticsearch import Elasticsearch
from django.conf import settings


class ElasticsearchService:
    def __init__(self):
        self.client = Elasticsearch([
            f"http://{settings.ELASTICSEARCH_HOST}:{settings.ELASTICSEARCH_PORT}"
        ])
        self.index_prefix = settings.ELASTICSEARCH_INDEX_PREFIX
    
    def create_index(self, index_name, mappings=None):
        full_index_name = f"{self.index_prefix}_{index_name}"
        if not self.client.indices.exists(index=full_index_name):
            self.client.indices.create(index=full_index_name, body=mappings)
    
    def index_document(self, index_name, doc_id, document):
        full_index_name = f"{self.index_prefix}_{index_name}"
        return self.client.index(index=full_index_name, id=doc_id, document=document)
    
    def search(self, index_name, query):
        full_index_name = f"{self.index_prefix}_{index_name}"
        return self.client.search(index=full_index_name, body=query)
    
    def delete_document(self, index_name, doc_id):
        full_index_name = f"{self.index_prefix}_{index_name}"
        return self.client.delete(index=full_index_name, id=doc_id)
