import logging

from api.schemas import EvaluationScore
from core.config import settings
from refinery.llm_client import GroqClient
from refinery.strategies.hyde import HyDE
from refinery.strategies.multi_query import MultiQuery
from refinery.strategies.query_decomposer import QueryDecomposer
from refinery.strategies.query_rewriter import QueryRewriter

logger = logging.getLogger(__name__)

CLASSIFY_PROMPT = """Given this user query, select the best pre-retrieval strategy:

- query_rewriter: query is ambiguous, has pronouns ("it", "they"), refers to previous context, or has grammar issues
- hyde: query asks for factual, descriptive, or explanatory information where a hypothetical document would help
- multi_query: query would benefit from multiple search angles or covers a broad topic
- query_decomposer: query contains multiple distinct questions joined by "and", "or", "also", or lists

Query: {query}

Respond with ONLY the strategy name (one of: query_rewriter, hyde, multi_query, query_decomposer):"""

EVALUATE_PROMPT = """Compare the raw and refined versions of a search query on three criteria (score 1-10):

Criterion 1 — Clarity: How clear and well-formed is the query?
Criterion 2 — Specificity: How specific and detailed is the query?
Criterion 3 — Search-readiness: How effective would this query be for finding relevant documents?

Raw query: {raw}
Refined query: {refined}

Respond in this exact format:
Clarity: raw=X refined=Y — explanation
Specificity: raw=X refined=Y — explanation
Search-readiness: raw=X refined=Y — explanation"""


class RefineryEngine:
    def __init__(self):
        self.llm = GroqClient()
        self.strategies = {
            "query_rewriter": QueryRewriter(),
            "hyde": HyDE(),
            "multi_query": MultiQuery(),
            "query_decomposer": QueryDecomposer(),
        }

    def refine(
        self,
        query: str,
        strategy: str | None = None,
        conversation_history: list[str] | None = None,
    ):
        strategy_name = strategy or settings.refinery_default_strategy

        if strategy_name == "auto":
            return self.auto_refine(query, conversation_history)

        if strategy_name not in self.strategies:
            raise ValueError(f"Unknown strategy: {strategy_name}. Choose from: {list(self.strategies.keys())}, auto")

        result = self.strategies[strategy_name].refine(query=query, conversation_history=conversation_history)
        return {
            "original_query": query,
            "refined_queries": result.refined_queries,
            "strategy": result.strategy,
            "explanation": result.explanation,
            "metadata": result.metadata,
        }

    def auto_refine(self, query: str, conversation_history: list[str] | None = None):
        prompt = CLASSIFY_PROMPT.format(query=query)
        classification = self.llm.generate(prompt).strip().lower()

        strategy_name = classification.strip()
        if strategy_name not in self.strategies:
            logger.warning(f"LLM returned unknown strategy '{classification}', defaulting to query_rewriter")
            strategy_name = "query_rewriter"

        result = self.strategies[strategy_name].refine(query=query, conversation_history=conversation_history)
        return {
            "original_query": query,
            "refined_queries": result.refined_queries,
            "strategy": result.strategy,
            "explanation": f"Auto-selected: {strategy_name}. {result.explanation}",
            "metadata": {**result.metadata, "auto_classification": classification},
        }

    def evaluate(
        self,
        query: str,
        strategy: str | None = None,
        conversation_history: list[str] | None = None,
    ):
        strategy_name = strategy or settings.refinery_default_strategy
        raw_queries = [query]

        if strategy_name == "auto":
            refine_result = self.auto_refine(query, conversation_history)
        else:
            refine_result = self.refine(query, strategy_name, conversation_history)

        refined_queries = refine_result["refined_queries"]
        refined_text = refined_queries[0] if refined_queries else query

        prompt = EVALUATE_PROMPT.format(raw=query, refined=refined_text)
        eval_raw = self.llm.generate(prompt).strip()

        scores = self._parse_evaluation(eval_raw)

        return {
            "original_query": query,
            "raw_queries": raw_queries,
            "refined_queries": refined_queries,
            "strategy": refine_result["strategy"],
            "scores": scores,
        }

    def _parse_evaluation(self, text: str) -> list[dict]:
        scores = []
        for line in text.strip().split("\n"):
            line = line.strip()
            if not line:
                continue
            for criterion in ["Clarity", "Specificity", "Search-readiness"]:
                if line.startswith(criterion + ":"):
                    try:
                        raw_part = line.split("raw=")[1].split(" refined=")[0].strip()
                        refined_part = line.split("refined=")[1].split(" —")[0].strip() if " —" in line else line.split("refined=")[1].split(" ")[0].strip()
                        explanation = line.split("—", 1)[1].strip() if "—" in line else ""
                        scores.append(
                            EvaluationScore(
                                criterion=criterion,
                                raw_score=int(raw_part),
                                refined_score=int(refined_part),
                                explanation=explanation,
                            )
                        )
                    except (IndexError, ValueError):
                        continue
        return scores
