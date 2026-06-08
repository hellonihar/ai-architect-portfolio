import logging
import time

from agentic.llm_client import LLMClient
from agentic.strategies.adaptive_rag import AdaptiveRAG
from agentic.strategies.corrective_rag import CorrectiveRAG
from agentic.strategies.multi_hop import MultiHop
from agentic.strategies.self_rag import SelfRAG
from api.schemas import AgenticResponse, ReflectionStep
from retrieval.engine import RetrievalEngine

logger = logging.getLogger(__name__)


class AgenticEngine:
    def __init__(self, retrieval: RetrievalEngine):
        self.retrieval = retrieval
        self.llm = LLMClient()

        self.self_rag = SelfRAG(self.llm, retrieval)
        self.corrective_rag = CorrectiveRAG(self.llm, retrieval)
        self.adaptive_rag = AdaptiveRAG(self.llm, retrieval)
        self.multi_hop = MultiHop(self.llm, retrieval)

        self.strategies = {
            "self_rag": self.self_rag,
            "corrective_rag": self.corrective_rag,
            "adaptive_rag": self.adaptive_rag,
            "multi_hop": self.multi_hop,
        }

    def search(self, query: str, top_k: int = 10) -> AgenticResponse:
        return self.self_rag.execute(query, top_k=top_k)

    def correct(self, query: str, top_k: int = 10) -> AgenticResponse:
        return self.corrective_rag.execute(query, top_k=top_k)

    def adaptive(self, query: str, top_k: int = 10, complexity_threshold: float = 0.7) -> AgenticResponse:
        return self.adaptive_rag.execute(query, top_k=top_k, complexity_threshold=complexity_threshold)

    def multihop(self, query: str, top_k: int = 5, max_hops: int = 3) -> AgenticResponse:
        return self.multi_hop.execute(query, top_k=top_k, max_hops=max_hops)

    def auto(self, query: str, top_k: int = 10) -> AgenticResponse:
        start = time.perf_counter()

        strategy_name = self.llm.select_strategy(query)
        reflections = [
            ReflectionStep(
                step_type="strategy_selection",
                input=f"Query: {query}",
                output=f"Selected strategy: {strategy_name}",
                confidence=0.7,
                metadata={"selected_strategy": strategy_name},
            )
        ]

        strategy = self.strategies.get(strategy_name)
        if strategy is None:
            strategy = self.self_rag

        response = strategy.execute(query, top_k=top_k)
        response.strategy = "auto"
        response.reflections = reflections + response.reflections
        response.timing_ms = round((time.perf_counter() - start) * 1000, 1)

        return response

    @property
    def available_strategies(self) -> list[str]:
        return list(self.strategies.keys())

    @property
    def llm_available(self) -> bool:
        return self.llm.is_available
