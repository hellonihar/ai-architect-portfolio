from rank_bm25 import BM25Okapi

from retrieval.retrievers.base import BaseRetriever


class SparseRetriever(BaseRetriever):
    def __init__(self, documents: list[dict]):
        self.documents = documents
        self._bm25: BM25Okapi | None = None

    def _build_index(self):
        tokenized = [d["content"].lower().split() for d in self.documents]
        self._bm25 = BM25Okapi(tokenized)

    def retrieve(self, query: str, top_k: int = 10) -> list[dict]:
        if self._bm25 is None:
            self._build_index()

        tokenized_query = query.lower().split()
        scores = self._bm25.get_scores(tokenized_query)
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]

        results = []
        for idx in top_indices:
            results.append({
                "id": self.documents[idx]["id"],
                "content": self.documents[idx]["content"],
                "score": float(scores[idx]),
                "route": "sparse",
                "metadata": {"category": self.documents[idx].get("category", "")},
            })
        return results
