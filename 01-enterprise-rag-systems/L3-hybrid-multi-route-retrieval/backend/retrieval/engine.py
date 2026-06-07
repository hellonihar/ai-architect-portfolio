import logging
import time

from api.schemas import Document, RouteDecision
from core.config import settings
from data.sample_corpus import CATEGORIES, get_documents
from retrieval.embedder import Embedder
from retrieval.fusion.contextual import ContextualFusion
from retrieval.fusion.rrf import RRFFusion
from retrieval.fusion.weighted import WeightedFusion
from retrieval.retrievers.dense import DenseRetriever
from retrieval.retrievers.graph import GraphRetriever
from retrieval.retrievers.hybrid import HybridRetriever
from retrieval.retrievers.sparse import SparseRetriever
from retrieval.routing.classifier import ClassifierRouter
from retrieval.routing.router import QueryRouter

logger = logging.getLogger(__name__)


class RetrievalEngine:
    def __init__(self):
        self.documents = get_documents()
        self.entity_map = {cat: data["entities"] for cat, data in CATEGORIES.items()}

        self.embedder = Embedder()

        self.dense = DenseRetriever(self.embedder, self.documents)
        self.sparse = SparseRetriever(self.documents)
        self.graph = GraphRetriever(self.documents, self.entity_map)
        self.hybrid = HybridRetriever(self.dense, self.sparse)

        self.retrievers = {
            "dense": self.dense,
            "sparse": self.sparse,
            "graph": self.graph,
            "hybrid": self.hybrid,
        }

        self.fusion_methods = {
            "rrf": RRFFusion(constant=settings.rrf_constant),
            "weighted": WeightedFusion(alpha=settings.hybrid_alpha),
            "contextual": ContextualFusion(),
        }

        groq_client = self._init_groq() if settings.groq_api_key else None
        classifier = ClassifierRouter(self.embedder, groq_client)
        self.router = QueryRouter(classifier)

    def _init_groq(self):
        try:
            from langchain_groq import ChatGroq
            return ChatGroq(
                model=settings.groq_model,
                temperature=settings.groq_temperature,
                api_key=settings.groq_api_key,
            )
        except Exception as e:
            logger.warning("Groq init failed: %s", e)
            return None

    def search(
        self,
        query: str,
        retriever_name: str = "hybrid",
        fusion_method: str = "",
        top_k: int = 10,
        alpha: float = 0.5,
    ) -> tuple[list[Document], RouteDecision | None, float]:
        start = time.perf_counter()

        retriever = self.retrievers.get(retriever_name)
        if retriever is None:
            raise ValueError(f"Unknown retriever: {retriever_name}. Choose from: {list(self.retrievers.keys())}")

        if not fusion_method:
            fusion_method = settings.fusion_method

        raw_results = retriever.retrieve(query, top_k * 2)

        if fusion_method == "rrf":
            fusion = self.fusion_methods["rrf"]
        elif fusion_method == "weighted":
            weighted = WeightedFusion(alpha=alpha)
            fusion = weighted
        elif fusion_method == "contextual":
            contextual = ContextualFusion()
            contextual.set_alpha(alpha)
            fusion = contextual
        else:
            fusion = None

        if fusion and retriever_name == "hybrid":
            dense_results = self.dense.retrieve(query, top_k * 2)
            sparse_results = self.sparse.retrieve(query, top_k * 2)
            fused = fusion.fuse([dense_results, sparse_results], top_k)
        elif fusion and retriever_name != "hybrid":
            fused = fusion.fuse([raw_results], top_k)
        else:
            fused = raw_results[:top_k]

        docs = [Document(**d) for d in fused]
        elapsed = (time.perf_counter() - start) * 1000

        return docs, None, elapsed

    def route_query(
        self,
        query: str,
        top_k: int = 10,
    ) -> tuple[list[Document], RouteDecision, float]:
        start = time.perf_counter()
        decision = self.router.route(query)

        all_results: list[list[dict]] = []
        for ret_name in decision.selected_retrievers:
            retriever = self.retrievers.get(ret_name)
            if retriever:
                all_results.append(retriever.retrieve(query, top_k * 2))

        if len(all_results) > 1 and decision.fusion_method:
            fusion = self.fusion_methods.get(decision.fusion_method, self.fusion_methods["rrf"])
            fused = fusion.fuse(all_results, top_k)
        elif all_results:
            fused = all_results[0][:top_k]
        else:
            fused = []

        docs = [Document(**d) for d in fused]
        elapsed = (time.perf_counter() - start) * 1000

        route_decision = RouteDecision(
            query=decision.query,
            classified_type=decision.classified_type,
            confidence=decision.confidence,
            selected_retrievers=decision.selected_retrievers,
            fusion_method=decision.fusion_method,
            explanation=decision.explanation,
        )

        return docs, route_decision, elapsed

    def compare_all(self, query: str, top_k: int = 10) -> dict[str, list[Document]]:
        results: dict[str, list[Document]] = {}
        for name, retriever in self.retrievers.items():
            docs = retriever.retrieve(query, top_k)
            results[name] = [Document(**d) for d in docs]
        return results

    @property
    def available_retrievers(self) -> list[str]:
        return list(self.retrievers.keys())

    @property
    def available_fusion(self) -> list[str]:
        return list(self.fusion_methods.keys())

    @property
    def corpus_size(self) -> int:
        return len(self.documents)

    @property
    def graph_nodes(self) -> int:
        return self.graph.num_nodes

    @property
    def graph_edges(self) -> int:
        return self.graph.num_edges
