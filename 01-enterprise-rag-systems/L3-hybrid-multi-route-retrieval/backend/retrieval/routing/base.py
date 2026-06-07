from abc import ABC, abstractmethod


class ClassifierResult:
    def __init__(
        self,
        query_type: str,
        confidence: float,
        explanation: str = "",
    ):
        self.query_type = query_type
        self.confidence = confidence
        self.explanation = explanation


class BaseClassifier(ABC):
    @abstractmethod
    def classify(self, query: str) -> ClassifierResult:
        ...


class RouterDecision:
    def __init__(
        self,
        query: str,
        classified_type: str,
        confidence: float,
        selected_retrievers: list[str],
        fusion_method: str,
        explanation: str = "",
    ):
        self.query = query
        self.classified_type = classified_type
        self.confidence = confidence
        self.selected_retrievers = selected_retrievers
        self.fusion_method = fusion_method
        self.explanation = explanation


class BaseRouter(ABC):
    @abstractmethod
    def route(self, query: str) -> RouterDecision:
        ...
