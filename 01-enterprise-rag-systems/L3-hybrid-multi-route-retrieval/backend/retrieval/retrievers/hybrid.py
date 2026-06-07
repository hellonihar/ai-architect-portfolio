from retrieval.retrievers.base import BaseRetriever
from retrieval.retrievers.dense import DenseRetriever
from retrieval.retrievers.sparse import SparseRetriever


class HybridRetriever(BaseRetriever):
    def __init__(self, dense: DenseRetriever, sparse: SparseRetriever):
        self.dense = dense
        self.sparse = sparse

    def retrieve(self, query: str, top_k: int = 10) -> list[dict]:
        dense_results = self.dense.retrieve(query, top_k)
        sparse_results = self.sparse.retrieve(query, top_k)
        seen: dict[str, dict] = {}
        for doc in dense_results:
            doc["route"] = "hybrid:dense"
            seen[doc["id"]] = doc
        for doc in sparse_results:
            if doc["id"] in seen:
                seen[doc["id"]]["score"] += doc["score"]
                seen[doc["id"]]["route"] = "hybrid:both"
            else:
                doc["route"] = "hybrid:sparse"
                seen[doc["id"]] = doc
        results = sorted(seen.values(), key=lambda x: x["score"], reverse=True)
        return results[:top_k]
