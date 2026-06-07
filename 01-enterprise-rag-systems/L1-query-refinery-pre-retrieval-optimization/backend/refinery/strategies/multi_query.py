from core.config import settings
from refinery.llm_client import GroqClient
from refinery.strategies.base import BaseStrategy, RefinementResult

MULTI_QUERY_SYSTEM_PROMPT = """You are a search query expansion assistant. Generate {num_variants} different versions of the user's query.

Rules:
- Each variant should rephrase the same intent differently
- Vary wording, structure, and specificity across variants
- Each variant must be self-contained and search-ready
- Return one query per line, no numbering or bullets"""

MULTI_QUERY_PROMPT_TEMPLATE = """Generate {num_variants} distinct search queries for:

{query}

Each on a new line:"""


class MultiQuery(BaseStrategy):
    def __init__(self):
        self.llm = GroqClient()

    def refine(self, query: str, **kwargs) -> RefinementResult:
        num_variants = settings.multi_query_variants

        prompt = (
            MULTI_QUERY_SYSTEM_PROMPT.format(num_variants=num_variants)
            + "\n\n"
            + MULTI_QUERY_PROMPT_TEMPLATE.format(num_variants=num_variants, query=query)
        )
        raw = self.llm.generate(prompt).strip()
        variants = [line.strip("- ").strip() for line in raw.split("\n") if line.strip()]

        all_queries = [query] + variants[:num_variants]

        return RefinementResult(
            refined_queries=all_queries,
            strategy="multi_query",
            explanation=f"Expanded into {len(all_queries)} query variants for broader retrieval coverage",
            metadata={"num_variants": len(all_queries), "original_query": query},
        )
