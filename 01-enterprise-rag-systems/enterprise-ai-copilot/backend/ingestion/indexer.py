import logging

from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone, ServerlessSpec

from core.config import settings

logger = logging.getLogger(__name__)


class PineconeIndexer:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.embedding_model
        )
        self.pc = Pinecone(api_key=settings.pinecone_api_key)
        self._ensure_index()

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

    def index(self, chunks: list[dict]) -> int:
        texts = [c["content"] for c in chunks]
        metadatas = [c["metadata"] for c in chunks]
        vector_store = PineconeVectorStore.from_texts(
            texts=texts,
            embedding=self.embeddings,
            metadatas=metadatas,
            index_name=settings.pinecone_index,
            pinecone_api_key=settings.pinecone_api_key
        )
        logger.info(f"Indexed {len(texts)} chunks into Pinecone")
        return len(texts)
