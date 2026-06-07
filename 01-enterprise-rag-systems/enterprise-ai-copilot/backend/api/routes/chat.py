import logging

from fastapi import APIRouter, HTTPException

from api.schemas import ChatRequest, ChatResponse
from governance.guardrails import InputGuard, OutputGuard
from governance.audit import AuditLogger
from core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()
input_guard = InputGuard()
output_guard = OutputGuard()
audit = AuditLogger()
pipeline = None


def get_pipeline():
    global pipeline
    if pipeline is None:
        from rag.pipeline import RAGPipeline
        pipeline = RAGPipeline()
    return pipeline


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if settings.enable_guardrails:
        valid, error = input_guard.check(request.query)
        if not valid:
            raise HTTPException(status_code=400, detail=error)

    result = get_pipeline().run(
        query=request.query,
        conversation_id=request.conversation_id,
        top_k=request.top_k
    )

    if settings.enable_guardrails:
        valid, error = output_guard.check(result["answer"])
        if not valid:
            result["answer"] = "I generated an empty response. Please try rephrasing your question."

    if settings.enable_audit:
        audit.log_query(
            query=request.query,
            conversation_id=result["conversation_id"],
            status="success",
            processing_time_ms=result["processing_time_ms"]
        )

    return ChatResponse(**result)
