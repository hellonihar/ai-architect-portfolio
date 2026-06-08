import numpy as np

from retrieval.embedder import Embedder
from retrieval.retrievers.base import BaseRetriever


class DenseRetriever(BaseRetriever):
    def __init__(self, embedder: Embedder, documents: list[dict]):
        self.embedder = embedder
        self.documents = documents
        self._doc_embeddings: np.ndarray | None = None

    def _build_index(self):
        texts = [d["content"] for d in self.documents]
        self._doc_embeddings = self.embedder.embed(texts)

    def retrieve(self, query: str, top_k: int = 10) -> list[dict]:
        if self._doc_embeddings is None:
            self._build_index()

        query_vec = self.embedder.embed_single(query)
        scores = np.dot(self._doc_embeddings, query_vec)
        top_indices = np.argsort(scores)[::-1][:top_k]

        results = []
        for idx in top_indices:
            results.append({
                "id": self.documents[idx]["id"],
                "content": self.documents[idx]["content"],
                "score": float(scores[idx]),
                "route": "dense",
                "metadata": {"category": self.documents[idx].get("category", "")},
            })
        return results
