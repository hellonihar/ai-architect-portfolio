from abc import ABC, abstractmethod


class RefinementResult:
    def __init__(
        self,
        refined_documents: list[dict],
        strategy: str,
        explanation: str | None = None,
        metadata: dict | None = None,
    ):
        self.refined_documents = refined_documents
        self.strategy = strategy
        self.explanation = explanation
        self.metadata = metadata or {}


class BaseStrategy(ABC):
    @abstractmethod
    def refine(self, query: str, documents: list[dict], **kwargs) -> RefinementResult:
        ...
