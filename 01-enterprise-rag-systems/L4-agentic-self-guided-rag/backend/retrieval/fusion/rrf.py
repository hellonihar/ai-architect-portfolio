from retrieval.fusion.base import BaseFusion


class RRFFusion(BaseFusion):
    def __init__(self, constant: int = 60):
        self.constant = constant

    def fuse(self, result_lists: list[list[dict]], top_k: int = 10) -> list[dict]:
        scores: dict[str, dict] = {}
        for rank_list in result_lists:
            for rank, doc in enumerate(rank_list):
                doc_id = doc["id"]
                if doc_id not in scores:
                    scores[doc_id] = {"doc": doc, "rrf_score": 0.0}
                scores[doc_id]["rrf_score"] += 1.0 / (self.constant + rank + 1)

        ranked = sorted(scores.values(), key=lambda x: x["rrf_score"], reverse=True)
        for item in ranked:
            item["doc"]["score"] = round(item["rrf_score"], 4)

        return [item["doc"] for item in ranked[:top_k]]

    @property
    def name(self) -> str:
        return "rrf"
