from core.config import settings
from refinery.embedder import Embedder
from refinery.llm_client import GroqClient
from refinery.strategies.base import BaseStrategy, RefinementResult

HYDE_SYSTEM_PROMPT = """You are a document analyst. Given a question, write a hypothetical document passage that would perfectly answer it.

Rules:
- Write 2-3 paragraphs of informative text that reads like a real knowledge-base article
- Include specific details, numbers, and facts that would appear in a real document
- Do NOT mention that this is hypothetical or generated
- Do NOT reference the question directly — just write the passage as if it exists"""

HYDE_PROMPT_TEMPLATE = """Write a passage that answers this question:

{query}

Passage:"""


class HyDE(BaseStrategy):
    def __init__(self):
        self.llm = GroqClient()
        self.embedder = Embedder()

    def refine(self, query: str, **kwargs) -> RefinementResult:
        prompt = f"{HYDE_SYSTEM_PROMPT}\n\n{HYDE_PROMPT_TEMPLATE.format(query=query)}"
        hypothetical_doc = self.llm.generate(prompt).strip()

        embedding = self.embedder.embed(hypothetical_doc)

        return RefinementResult(
            refined_queries=[hypothetical_doc],
            strategy="hyde",
            explanation="Generated a hypothetical document to use as the search query embedding",
            metadata={
                "embedding": embedding,
                "embedding_dimension": len(embedding),
                "embedding_model": settings.embedding_model,
            },
        )
