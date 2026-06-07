from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone, ServerlessSpec

from core.config import settings
from rag.retrieval.base import BaseRetriever


class PineconeRetriever(BaseRetriever):
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.embedding_model
        )
        self.pc = Pinecone(api_key=settings.pinecone_api_key)
        self._ensure_index()
        self.vector_store = PineconeVectorStore(
            index_name=settings.pinecone_index,
            embedding=self.embeddings,
            pinecone_api_key=settings.pinecone_api_key
        )

    def _ensure_index(self):
        existing = [idx.name for idx in self.pc.list_indexes()]
        if settings.pinecone_index not in existing:
            self.pc.create_index(
                name=settings.pinecone_index,
                dimension=384,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region=settings.pinecone_environment
                )
            )

    def retrieve(self, query: str, top_k: int = 5) -> list[dict]:
        docs = self.vector_store.similarity_search_with_score(
            query, k=top_k
        )
        return [
            {
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": score
            }
            for doc, score in docs
        ]
