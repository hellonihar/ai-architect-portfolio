import time
import uuid
import logging

from core.config import settings
from rag.retrieval.vector import PineconeRetriever
from rag.retrieval.reranker import Reranker
from rag.augmentation.context_builder import ContextBuilder
from rag.augmentation.prompt_templates import RAG_PROMPT
from rag.generation.groq_client import GroqLLM
from rag.generation.fallback import FallbackHandler
from rag.generation.response_formatter import ResponseFormatter

logger = logging.getLogger(__name__)


class RAGPipeline:
    def __init__(self):
        self.retriever = PineconeRetriever()
        self.reranker = Reranker()
        self.context_builder = ContextBuilder()
        self.llm = GroqLLM()
        self.fallback_handler = FallbackHandler(self.llm)
        self.formatter = ResponseFormatter()

    def run(
        self,
        query: str,
        conversation_id: str | None = None,
        top_k: int | None = None
    ) -> dict:
        start = time.time()
        conv_id = conversation_id or str(uuid.uuid4())
        k = top_k or settings.top_k

        retrieved = self.retriever.retrieve(query, top_k=k)
        ranked = self.reranker.rerank(query, retrieved, top_k=settings.rerank_top_k)
        context = self.context_builder.build(ranked, max_length=settings.max_input_length)
        sources = self.context_builder.format_sources(ranked)

        prompt = RAG_PROMPT.invoke({"context": context, "query": query})
        answer = self.fallback_handler.generate_with_fallback(prompt)

        elapsed = (time.time() - start) * 1000

        return self.formatter.format(
            answer=answer,
            sources=sources,
            conversation_id=conv_id,
            processing_time_ms=elapsed
        )
