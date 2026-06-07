import logging

from refiner.retriever import InMemoryRetriever
from refiner.strategies.base import BaseStrategy, RefinementResult

logger = logging.getLogger(__name__)


class SmallToBig(BaseStrategy):
    def __init__(self, retriever: InMemoryRetriever):
        self.retriever = retriever

    def refine(self, query: str, documents: list[dict], **kwargs) -> RefinementResult:
        if not documents:
            return RefinementResult(
                refined_documents=[],
                strategy="small_to_big",
                explanation="No documents to expand",
            )

        parent_ids = set()
        for doc in documents:
            pid = doc.get("parent_id")
            if pid:
                parent_ids.add(pid)

        expanded = []
        for pid in parent_ids:
            content = self.retriever.get_parent_content(pid)
            if content:
                expanded.append({
                    "id": f"parent-{pid}",
                    "content": content,
                    "score": max(
                        (d["score"] for d in documents if d.get("parent_id") == pid),
                        default=0.0,
                    ),
                    "parent_id": pid,
                    "metadata": {
                        "expanded_from": [d["id"] for d in documents if d.get("parent_id") == pid],
                        "child_count": sum(1 for d in documents if d.get("parent_id") == pid),
                    },
                })

        expansion_ratio = len(expanded) / len(documents) if documents else 0

        return RefinementResult(
            refined_documents=expanded,
            strategy="small_to_big",
            explanation=f"Expanded {len(documents)} child chunks into {len(expanded)} parent documents ",
            metadata={
                "child_chunks": len(documents),
                "parent_documents": len(expanded),
                "expansion_ratio": round(expansion_ratio, 2),
                "parent_ids": list(parent_ids),
            },
        )
