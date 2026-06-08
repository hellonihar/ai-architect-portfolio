import logging

from agentic.llm_client import LLMClient
from api.schemas import ReflectionStep

logger = logging.getLogger(__name__)


class CitationChecker:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def check(self, statement: str, passage: dict) -> tuple[str, float, str]:
        result = self.llm.check_citation(statement, passage["content"])
        label = result.get("label", "supported")
        confidence = result.get("confidence", 0.5)
        explanation = result.get("explanation", "")
        return label, confidence, explanation

    def verify_answer(
        self, answer: str, passages: list[dict]
    ) -> tuple[list[str], list[ReflectionStep]]:
        verified_citations = []
        reflections = []

        for passage in passages:
            label, confidence, explanation = self.check(answer, passage)
            reflections.append(ReflectionStep(
                step_type="reflect_citation",
                input=f"Statement excerpt: {answer[:300]}\nPassage: {passage['id']}",
                output=f"Label: {label}, Confidence: {confidence:.2f}, Explanation: {explanation}",
                confidence=confidence,
                metadata={"doc_id": passage["id"], "label": label},
            ))

            if label in ("supported", "partial"):
                verified_citations.append(passage["id"])

        return verified_citations, reflections
