import logging

from core.config import settings
from refiner.llm_client import GroqClient
from refiner.strategies.base import BaseStrategy, RefinementResult

logger = logging.getLogger(__name__)

COMPRESS_PROMPT = """You are a context compression assistant. Given a user query and a list of document chunks, your task is to:

1. Remove chunks that are irrelevant to the query
2. Merge chunks that contain redundant information
3. Keep the most informative content — preserve facts, numbers, and specific details

Query: {query}

Document chunks:
{documents}

Respond with the compressed/cleaned version. Keep only the content relevant to answering the query. If a chunk is entirely irrelevant, drop it entirely. If multiple chunks overlap, keep only the most detailed version.

Compressed context:"""


class Compressor(BaseStrategy):
    def __init__(self):
        self.llm = GroqClient()

    def refine(self, query: str, documents: list[dict], **kwargs) -> RefinementResult:
        if not documents:
            return RefinementResult(
                refined_documents=[],
                strategy="compressor",
                explanation="No documents to compress",
            )

        original_tokens = sum(len(d["content"].split()) for d in documents)

        doc_text = "\n\n".join(
            f"[Chunk {doc['id']}]\n{doc['content']}" for doc in documents
        )

        prompt = COMPRESS_PROMPT.format(query=query, documents=doc_text)
        compressed = self.llm.generate(prompt).strip()

        compressed_tokens = len(compressed.split())
        savings = ((original_tokens - compressed_tokens) / original_tokens * 100) if original_tokens > 0 else 0

        result_doc = {
            "id": "compressed",
            "content": compressed,
            "score": 1.0,
            "parent_id": None,
            "metadata": {
                "original_chunks": len(documents),
                "original_tokens": original_tokens,
                "compressed_tokens": compressed_tokens,
                "token_savings_pct": round(savings, 1),
            },
        }

        return RefinementResult(
            refined_documents=[result_doc],
            strategy="compressor",
            explanation=f"Compressed {len(documents)} chunks from {original_tokens} to {compressed_tokens} tokens ({round(savings, 1)}% reduction)",
            metadata={
                "original_chunk_count": len(documents),
                "original_tokens": original_tokens,
                "compressed_tokens": compressed_tokens,
                "token_savings_pct": round(savings, 1),
            },
        )
