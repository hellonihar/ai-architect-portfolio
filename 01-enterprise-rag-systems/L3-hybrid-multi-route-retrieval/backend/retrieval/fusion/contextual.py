from retrieval.fusion.weighted import WeightedFusion


class ContextualFusion(WeightedFusion):
    def __init__(self):
        super().__init__(alpha=0.5)
        self._alpha = 0.5

    @property
    def name(self) -> str:
        return "contextual"

    def set_alpha(self, alpha: float):
        self._alpha = max(0.0, min(1.0, alpha))

    def fuse(self, result_lists: list[list[dict]], top_k: int = 10) -> list[dict]:
        return super().fuse(result_lists, top_k)
