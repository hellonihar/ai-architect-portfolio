import numpy as np

from retrieval.embedder import Embedder
from retrieval.retrievers.base import BaseRetriever


class DenseRetriever(BaseRetriever):
    def __init__(self, embedder: Embedder, documents: list[dict]):
        self.embedder = embedder
        self.documents = documents
        self.doc_texts = [d["content"] for d in documents]
        self.doc_ids = [d["id"] for d in documents]
        self.embeddings = embedder.encode(self.doc_texts)
        self.embeddings_np = np.array(self.embeddings)

    def retrieve(self, query: str, top_k: int = 10) -> list[dict]:
        query_emb = np.array(self.embedder.encode_single(query))
        scores = self.embeddings_np @ query_emb
        top_indices = np.argsort(scores)[::-1][:top_k]
        results = []
        for idx in top_indices:
            doc = self.documents[idx]
            results.append({
                "id": doc["id"],
                "content": doc["content"],
                "score": float(scores[idx]),
                "route": "dense",
                "metadata": {"category": doc.get("category", "")},
            })
        return results
