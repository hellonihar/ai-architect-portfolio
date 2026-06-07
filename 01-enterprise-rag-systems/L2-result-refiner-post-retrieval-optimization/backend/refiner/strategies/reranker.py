import logging

from core.config import settings
from refiner.cross_encoder import CrossEncoderClient
from refiner.strategies.base import BaseStrategy, RefinementResult

logger = logging.getLogger(__name__)


class Reranker(BaseStrategy):
    def __init__(self):
        self.cross_encoder = CrossEncoderClient()

    def refine(self, query: str, documents: list[dict], **kwargs) -> RefinementResult:
        if not documents:
            return RefinementResult(
                refined_documents=[],
                strategy="reranker",
                explanation="No documents to rerank",
            )

        pairs = [(query, doc["content"]) for doc in documents]
        cross_scores = self.cross_encoder.score(pairs)

        for doc, score in zip(documents, cross_scores):
            doc["cross_encoder_score"] = round(score, 4)

        reranked = sorted(documents, key=lambda d: d["cross_encoder_score"], reverse=True)

        position_changes = []
        for new_pos, doc in enumerate(reranked):
            old_pos = next(i for i, d in enumerate(documents) if d["id"] == doc["id"])
            change = old_pos - new_pos
            if change != 0:
                position_changes.append({"id": doc["id"], "from": old_pos, "to": new_pos, "change": change})

        reranked = reranked[: settings.rerank_top_k]

        return RefinementResult(
            refined_documents=reranked,
            strategy="reranker",
            explanation=f"Re-ranked {len(documents)} documents using cross-encoder. Top {settings.rerank_top_k} selected.",
            metadata={
                "position_changes": position_changes,
                "original_top_k": len(documents),
                "rerank_top_k": settings.rerank_top_k,
                "cross_encoder_model": settings.cross_encoder_model,
            },
        )
