import logging

from core.config import settings
from refiner.strategies.base import BaseStrategy, RefinementResult

logger = logging.getLogger(__name__)


class SlidingWindow(BaseStrategy):
    def refine(self, query: str, documents: list[dict], **kwargs) -> RefinementResult:
        if not documents:
            return RefinementResult(
                refined_documents=[],
                strategy="sliding_window",
                explanation="No documents to process",
            )

        threshold = kwargs.get("threshold", settings.sliding_window_threshold)
        token_budget = kwargs.get("token_budget", settings.sliding_window_token_budget)

        sorted_docs = sorted(documents, key=lambda d: d["score"], reverse=True)

        selected = []
        dropped = []
        total_tokens = 0

        for doc in sorted_docs:
            doc_tokens = len(doc["content"].split())

            if doc["score"] < threshold:
                dropped.append({**doc, "drop_reason": f"score {doc['score']:.3f} below threshold {threshold}"})
                continue

            if total_tokens + doc_tokens > token_budget:
                dropped.append({**doc, "drop_reason": f"exceeds token budget ({token_budget})"})
                continue

            selected.append(doc)
            total_tokens += doc_tokens

        return RefinementResult(
            refined_documents=selected,
            strategy="sliding_window",
            explanation=f"Selected {len(selected)}/{len(documents)} chunks within budget ({total_tokens}/{token_budget} tokens, threshold={threshold})",
            metadata={
                "total_candidates": len(documents),
                "selected": len(selected),
                "dropped": len(dropped),
                "total_tokens": total_tokens,
                "token_budget": token_budget,
                "threshold": threshold,
                "dropped_documents": dropped,
            },
        )
