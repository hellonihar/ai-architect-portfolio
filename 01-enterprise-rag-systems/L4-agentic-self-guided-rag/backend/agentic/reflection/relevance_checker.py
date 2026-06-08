import logging

from agentic.llm_client import LLMClient
from api.schemas import ReflectionStep

logger = logging.getLogger(__name__)


class RelevanceChecker:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def check(self, query: str, passage: dict) -> tuple[str, float, str]:
        result = self.llm.check_relevance(query, passage["content"])
        label = result.get("label", "relevant")
        confidence = result.get("confidence", 0.5)
        explanation = result.get("explanation", "")
        return label, confidence, explanation

    def filter_relevant(self, query: str, passages: list[dict], threshold: float = 0.5) -> tuple[list[dict], list[ReflectionStep]]:
        relevant = []
        reflections = []

        for passage in passages:
            label, confidence, explanation = self.check(query, passage)
            reflections.append(ReflectionStep(
                step_type="reflect_relevance",
                input=f"Query: {query}\nPassage: {passage['id']}",
                output=f"Label: {label}, Confidence: {confidence:.2f}, Explanation: {explanation}",
                confidence=confidence,
                metadata={"doc_id": passage["id"], "label": label},
            ))

            if label == "relevant" or (label == "partial" and confidence >= threshold):
                relevant.append(passage)

        logger.info("Relevance: %d/%d passages retained", len(relevant), len(passages))
        return relevant, reflections
