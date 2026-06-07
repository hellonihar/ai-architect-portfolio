from core.config import settings
from refinery.llm_client import GroqClient
from refinery.strategies.base import BaseStrategy, RefinementResult

REWRITE_SYSTEM_PROMPT = """You are a query rewriting assistant. Your task is to rewrite the user's query to be more specific, search-friendly, and self-contained.

Rules:
- Fix spelling and grammar
- Expand abbreviations and acronyms
- Make implicit context explicit
- Keep the rewritten query concise (under 50 words)
- If conversation history is provided, use it to resolve pronouns and references
- Return ONLY the rewritten query, no explanation"""

REWRITE_PROMPT_TEMPLATE = """Conversation history:
{history}

Original query: {query}

Rewritten query:"""


class QueryRewriter(BaseStrategy):
    def __init__(self):
        self.llm = GroqClient()

    def refine(self, query: str, **kwargs) -> RefinementResult:
        history = kwargs.get("conversation_history", [])

        if settings.rewriter_use_history and history:
            history_text = "\n".join(history[-5:])
            prompt = f"{REWRITE_SYSTEM_PROMPT}\n\n{REWRITE_PROMPT_TEMPLATE.format(history=history_text, query=query)}"
            explanation = "Rewritten using conversation history for context resolution"
        else:
            prompt = f"{REWRITE_SYSTEM_PROMPT}\n\nOriginal query: {query}\n\nRewritten query:"
            explanation = "Rewritten for specificity and search-readiness"

        rewritten = self.llm.generate(prompt).strip()

        return RefinementResult(
            refined_queries=[rewritten],
            strategy="query_rewriter",
            explanation=explanation,
            metadata={"original_query": query, "used_history": bool(history and settings.rewriter_use_history)},
        )
