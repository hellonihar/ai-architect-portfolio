from abc import ABC, abstractmethod


class BaseRetriever(ABC):
    @abstractmethod
    def retrieve(self, query: str, top_k: int = 10) -> list[dict]:
        ...
