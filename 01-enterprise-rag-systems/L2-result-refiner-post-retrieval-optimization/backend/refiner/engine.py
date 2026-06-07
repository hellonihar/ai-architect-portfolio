import logging

from api.schemas import Document
from core.config import settings
from refiner.retriever import InMemoryRetriever
from refiner.strategies.compressor import Compressor
from refiner.strategies.reranker import Reranker
from refiner.strategies.sliding_window import SlidingWindow
from refiner.strategies.small_to_big import SmallToBig

logger = logging.getLogger(__name__)


def _to_document(doc: dict) -> Document:
    return Document(
        id=doc["id"],
        content=doc["content"],
        score=doc["score"],
        parent_id=doc.get("parent_id"),
        metadata=doc.get("metadata", {}),
    )


class RefinerEngine:
    def __init__(self):
        self.retriever = InMemoryRetriever()
        self.strategies = {
            "reranker": Reranker(),
            "compressor": Compressor(),
            "small_to_big": SmallToBig(self.retriever),
            "sliding_window": SlidingWindow(),
        }

    def refine(self, query: str, strategy: str = "reranker", top_k: int = 10):
        raw_results = self.retriever.retrieve(query, top_k)

        if strategy not in self.strategies:
            raise ValueError(f"Unknown strategy: {strategy}. Choose from: {list(self.strategies.keys())}")

        strategy_instance = self.strategies[strategy]
        result = strategy_instance.refine(query, raw_results)

        return {
            "original_query": query,
            "strategy": result.strategy,
            "raw_results": [_to_document(d) for d in raw_results],
            "refined_results": [_to_document(d) for d in result.refined_documents],
            "explanation": result.explanation,
            "metadata": result.metadata,
        }

    def evaluate(self, query: str, top_k: int = 10):
        raw_results = self.retriever.retrieve(query, top_k)

        strategies_output = {}
        for name, strategy_instance in self.strategies.items():
            try:
                result = strategy_instance.refine(query, raw_results)
                strategies_output[name] = {
                    "refined_results": [_to_document(d) for d in result.refined_documents],
                    "explanation": result.explanation,
                    "metadata": result.metadata,
                }
            except Exception as e:
                logger.error(f"Strategy {name} failed: {e}")
                strategies_output[name] = {
                    "refined_results": [],
                    "explanation": f"Failed: {str(e)}",
                    "metadata": {},
                }

        return {
            "original_query": query,
            "raw_results": [_to_document(d) for d in raw_results],
            "strategies": strategies_output,
        }
