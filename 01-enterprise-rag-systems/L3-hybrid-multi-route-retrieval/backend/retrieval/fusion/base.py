from abc import ABC, abstractmethod


class BaseFusion(ABC):
    @abstractmethod
    def fuse(self, result_lists: list[list[dict]], top_k: int = 10) -> list[dict]:
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        ...
