from abc import ABC, abstractmethod


class RefinementResult:
    def __init__(
        self,
        refined_queries: list[str],
        strategy: str,
        explanation: str | None = None,
        metadata: dict | None = None,
    ):
        self.refined_queries = refined_queries
        self.strategy = strategy
        self.explanation = explanation
        self.metadata = metadata or {}


class BaseStrategy(ABC):
    @abstractmethod
    def refine(self, query: str, **kwargs) -> RefinementResult:
        ...
