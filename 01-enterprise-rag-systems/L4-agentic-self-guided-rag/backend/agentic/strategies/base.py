from abc import ABC, abstractmethod

from api.schemas import AgenticResponse


class BaseAgenticStrategy(ABC):
    @abstractmethod
    def execute(self, query: str, top_k: int = 10, **kwargs) -> AgenticResponse:
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        ...
