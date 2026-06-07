from retrieval.fusion.base import BaseFusion


class RRFFusion(BaseFusion):
    def __init__(self, constant: int = 60):
        self._constant = constant

    @property
    def name(self) -> str:
        return "rrf"

    def fuse(self, result_lists: list[list[dict]], top_k: int = 10) -> list[dict]:
        rrf_scores: dict[str, dict] = {}
        for doc_list in result_lists:
            for rank, doc in enumerate(doc_list):
                doc_id = doc["id"]
                rrf_score = 1.0 / (self._constant + rank + 1)
                if doc_id in rrf_scores:
                    rrf_scores[doc_id]["score"] += rrf_score
                else:
                    entry = doc.copy()
                    entry["score"] = rrf_score
                    entry["fusion_contributions"] = 1
                    rrf_scores[doc_id] = entry
        results = sorted(rrf_scores.values(), key=lambda x: x["score"], reverse=True)
        return results[:top_k]
