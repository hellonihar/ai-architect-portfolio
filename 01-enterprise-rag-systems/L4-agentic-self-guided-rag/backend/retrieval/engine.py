import logging
import time

from api.schemas import Document
from core.config import settings
from data.sample_corpus import CATEGORIES, get_documents
from retrieval.embedder import Embedder
from retrieval.fusion.rrf import RRFFusion
from retrieval.retrievers.dense import DenseRetriever
from retrieval.retrievers.sparse import SparseRetriever

logger = logging.getLogger(__name__)


class RetrievalEngine:
    def __init__(self):
        self.documents = get_documents()

        self.embedder = Embedder()

        self.dense = DenseRetriever(self.embedder, self.documents)
        self.sparse = SparseRetriever(self.documents)

        self.retrievers = {
            "dense": self.dense,
            "sparse": self.sparse,
        }

        self.fusion_methods = {
            "rrf": RRFFusion(constant=settings.rrf_constant),
        }

    def search(self, query: str, retriever_name: str = "hybrid", top_k: int = 10) -> tuple[list[Document], float]:
        start = time.perf_counter()

        if retriever_name == "hybrid":
            dense_results = self.dense.retrieve(query, top_k * 2)
            sparse_results = self.sparse.retrieve(query, top_k * 2)
            fused = self.fusion_methods["rrf"].fuse([dense_results, sparse_results], top_k)
        else:
            retriever = self.retrievers.get(retriever_name)
            if retriever is None:
                raise ValueError(f"Unknown retriever: {retriever_name}. Choose from: {list(self.retrievers.keys()) + ['hybrid']}")
            fused = retriever.retrieve(query, top_k)

        docs = [Document(**d) for d in fused]
        elapsed = (time.perf_counter() - start) * 1000
        return docs, elapsed

    @property
    def available_retrievers(self) -> list[str]:
        return list(self.retrievers.keys()) + ["hybrid"]

    @property
    def corpus_size(self) -> int:
        return len(self.documents)

    @property
    def corpus_categories(self) -> list[str]:
        return list(CATEGORIES.keys())
