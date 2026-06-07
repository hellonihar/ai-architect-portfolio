from refinery.llm_client import GroqClient
from refinery.strategies.base import BaseStrategy, RefinementResult

DECOMPOSE_SYSTEM_PROMPT = """You are a query decomposition assistant. Identify if the user's question contains multiple distinct sub-questions.

Rules:
- If the query asks about multiple topics, split it into individual sub-queries
- Each sub-query must be self-contained and independently answerable
- Return one sub-query per line, no numbering or bullets
- If the query is a single atomic question, return it unchanged"""

DECOMPOSE_PROMPT_TEMPLATE = """Decompose this query into atomic sub-queries:

{query}

Sub-queries:"""


class QueryDecomposer(BaseStrategy):
    def __init__(self):
        self.llm = GroqClient()

    def refine(self, query: str, **kwargs) -> RefinementResult:
        prompt = DECOMPOSE_SYSTEM_PROMPT + "\n\n" + DECOMPOSE_PROMPT_TEMPLATE.format(query=query)
        raw = self.llm.generate(prompt).strip()
        sub_queries = [line.strip("- ").strip() for line in raw.split("\n") if line.strip()]

        return RefinementResult(
            refined_queries=sub_queries,
            strategy="query_decomposer",
            explanation=f"Decomposed into {len(sub_queries)} atomic sub-queries"
            if len(sub_queries) > 1
            else "Query is atomic — no decomposition needed",
            metadata={"num_sub_queries": len(sub_queries), "original_query": query},
        )
