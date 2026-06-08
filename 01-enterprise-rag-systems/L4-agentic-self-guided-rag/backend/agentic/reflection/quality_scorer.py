import logging

from agentic.llm_client import LLMClient
from api.schemas import ReflectionStep

logger = logging.getLogger(__name__)


class QualityScorer:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def score(self, query: str, passages: list[dict]) -> tuple[str, float, str, ReflectionStep]:
        passage_texts = [p["content"] for p in passages]
        result = self.llm.score_quality(query, passage_texts)
        quality = result.get("quality", "medium")
        confidence = result.get("confidence", 0.5)
        explanation = result.get("explanation", "")

        reflection = ReflectionStep(
            step_type="score_quality",
            input=f"Query: {query}\nPassages count: {len(passages)}",
            output=f"Quality: {quality}, Confidence: {confidence:.2f}, Explanation: {explanation}",
            confidence=confidence,
            metadata={"quality": quality},
        )

        return quality, confidence, explanation, reflection

    def needs_correction(self, quality: str, threshold: str = "medium") -> tuple[bool, str]:
        quality_levels = {"high": 3, "medium": 2, "low": 1}
        threshold_level = quality_levels.get(threshold, 2)
        current_level = quality_levels.get(quality, 1)

        if current_level >= threshold_level:
            return False, "quality_sufficient"
        if current_level == 1:
            return True, "fallback_needed"
        return True, "rewrite_needed"
