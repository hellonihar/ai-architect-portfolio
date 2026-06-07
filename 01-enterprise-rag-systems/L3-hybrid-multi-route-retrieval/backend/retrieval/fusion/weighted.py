from retrieval.fusion.base import BaseFusion


class WeightedFusion(BaseFusion):
    def __init__(self, alpha: float = 0.5):
        self._alpha = alpha

    @property
    def name(self) -> str:
        return "weighted"

    def fuse(self, result_lists: list[list[dict]], top_k: int = 10) -> list[dict]:
        if not result_lists:
            return []
        if len(result_lists) == 1:
            return result_lists[0][:top_k]
        weights = [self._alpha, 1.0 - self._alpha]
        combined: dict[str, dict] = {}
        for weight, doc_list in zip(weights, result_lists):
            max_score = max((d["score"] for d in doc_list), default=1.0)
            min_score = min((d["score"] for d in doc_list), default=0.0)
            score_range = max_score - min_score if max_score != min_score else 1.0
            for doc in doc_list:
                doc_id = doc["id"]
                normalized = (doc["score"] - min_score) / score_range
                contribution = normalized * weight
                if doc_id in combined:
                    combined[doc_id]["score"] += contribution
                else:
                    entry = doc.copy()
                    entry["score"] = contribution
                    combined[doc_id] = entry
        results = sorted(combined.values(), key=lambda x: x["score"], reverse=True)
        return results[:top_k]
