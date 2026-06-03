from django.conf import settings
from pinecone import Pinecone, ServerlessSpec


class PineconeClient:
    def __init__(self):
        pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        index_name = settings.PINECONE_INDEX_NAME
        if index_name not in pc.list_indexes().names():
            pc.create_index(
                name=index_name,
                dimension=1536,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region=settings.PINECONE_ENVIRONMENT),
            )
        self.index = pc.Index(index_name)

    def upsert(self, vector_id, embedding, metadata=None):
        self.index.upsert(vectors=[(vector_id, embedding, metadata or {})])

    def query(self, embedding, top_k=10, filter=None):
        results = self.index.query(
            vector=embedding,
            top_k=top_k,
            filter=filter,
            include_metadata=True,
        )
        return [
            {"id": r["id"], "score": r["score"], "metadata": r.get("metadata", {})}
            for r in results["matches"]
        ]

    def delete(self, vector_id):
        self.index.delete(ids=[vector_id])


_client = None


def get_pinecone_client():
    global _client
    if _client is None:
        _client = PineconeClient()
    return _client


def upsert_embedding(vector_id, embedding, metadata=None):
    client = get_pinecone_client()
    client.upsert(vector_id, embedding, metadata)


def query_embeddings(embedding, top_k=10, filter=None):
    client = get_pinecone_client()
    return client.query(embedding, top_k, filter)
