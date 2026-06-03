from langchain.embeddings import OpenAIEmbeddings
from langchain.retrievers import EnsembleRetriever
from langchain.retrievers import BM25Retriever as LangChainBM25
from langchain.vectorstores import Pinecone as LangchainPinecone
from django.conf import settings
from .pinecone_client import get_pinecone_client


def get_embedding_function():
    return OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=settings.OPENAI_API_KEY,
    )


class HybridRetriever:
    def __init__(self):
        self.embedding_fn = get_embedding_function()
        self.pinecone = get_pinecone_client()

    def retrieve(self, query, top_k=10):
        query_embedding = self.embedding_fn.embed_query(query)

        # Semantic search
        vector_results = self.pinecone.query(query_embedding, top_k=top_k)

        # Keyword search (BM25)
        from .bm25 import BM25Search
        bm25 = BM25Search()
        keyword_results = bm25.search(query, top_k=top_k)

        # Reciprocal Rank Fusion
        return self._rrf(vector_results, keyword_results, top_k)

    def _rrf(self, vector_results, keyword_results, top_k, k=60):
        scores = {}
        for i, r in enumerate(vector_results):
            scores[r["id"]] = scores.get(r["id"], 0) + 1 / (k + i + 1)
        for i, r in enumerate(keyword_results):
            scores[r["id"]] = scores.get(r["id"], 0) + 1 / (k + i + 1)
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [{"id": doc_id, "score": score} for doc_id, score in ranked[:top_k]]
