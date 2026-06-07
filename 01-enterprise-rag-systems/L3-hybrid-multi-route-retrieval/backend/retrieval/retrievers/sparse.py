from rank_bm25 import BM25Okapi

from retrieval.retrievers.base import BaseRetriever


class SparseRetriever(BaseRetriever):
    def __init__(self, documents: list[dict]):
        self.documents = documents
        self.doc_texts = [d["content"] for d in documents]
        tokenized = [doc.lower().split() for doc in self.doc_texts]
        self.bm25 = BM25Okapi(tokenized)

    def retrieve(self, query: str, top_k: int = 10) -> list[dict]:
        tokenized_query = query.lower().split()
        scores = self.bm25.get_scores(tokenized_query)
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
        results = []
        for idx in top_indices:
            doc = self.documents[idx]
            results.append({
                "id": doc["id"],
                "content": doc["content"],
                "score": float(scores[idx]),
                "route": "sparse",
                "metadata": {"category": doc.get("category", "")},
            })
        return results
