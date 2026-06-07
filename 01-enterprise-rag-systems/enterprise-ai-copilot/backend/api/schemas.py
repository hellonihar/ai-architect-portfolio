from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=4096)
    conversation_id: Optional[str] = None
    top_k: Optional[int] = None


class Source(BaseModel):
    content: str
    metadata: dict


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]
    conversation_id: str
    processing_time_ms: float


class DocumentUploadResponse(BaseModel):
    document_id: str
    filename: str
    chunks_count: int
    status: str


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    top_k: int = 5


class SearchResult(BaseModel):
    content: str
    metadata: dict
    score: float
