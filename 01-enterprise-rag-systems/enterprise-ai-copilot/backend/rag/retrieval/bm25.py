from rag.retrieval.base import BaseRetriever


class BM25Retriever(BaseRetriever):
    def retrieve(self, query: str, top_k: int = 5) -> list[dict]:
        return []
