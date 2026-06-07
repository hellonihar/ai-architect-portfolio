from pydantic import BaseModel, Field


class Document(BaseModel):
    id: str
    content: str
    score: float
    parent_id: str | None = None
    metadata: dict = {}


class RefineRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=4096)
    strategy: str = "reranker"
    top_k: int = 10


class RefineResponse(BaseModel):
    original_query: str
    strategy: str
    raw_results: list[Document]
    refined_results: list[Document]
    explanation: str
    metadata: dict = {}


class EvaluateResponse(BaseModel):
    original_query: str
    raw_results: list[Document]
    strategies: dict
