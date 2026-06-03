from django.conf import settings
from elasticsearch import Elasticsearch


class BM25Search:
    def __init__(self):
        self.client = Elasticsearch(settings.ELASTICSEARCH_HOST)
        self.index_name = "enterprise_rag_documents"

    def index_document(self, doc_id, text, metadata=None):
        body = {"text": text, "metadata": metadata or {}}
        self.client.index(index=self.index_name, id=doc_id, body=body)

    def search(self, query, top_k=10):
        body = {
            "query": {"match": {"text": query}},
            "size": top_k,
        }
        response = self.client.search(index=self.index_name, body=body)
        results = []
        for hit in response["hits"]["hits"]:
            results.append({
                "id": hit["_id"],
                "score": hit["_score"],
                "text": hit["_source"]["text"],
                "metadata": hit["_source"].get("metadata", {}),
            })
        return results

    def delete_document(self, doc_id):
        self.client.delete(index=self.index_name, id=doc_id, ignore=[404])
