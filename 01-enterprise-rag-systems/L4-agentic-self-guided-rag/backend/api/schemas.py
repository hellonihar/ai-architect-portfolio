from pydantic import BaseModel, Field


class Document(BaseModel):
    id: str
    content: str
    score: float
    route: str = ""
    metadata: dict = {}


class ReflectionStep(BaseModel):
    step_type: str
    input: str
    output: str
    confidence: float
    metadata: dict = {}


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=4096)
    top_k: int = 10


class AdaptiveRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=4096)
    top_k: int = 10
    complexity_threshold: float = 0.7


class MultiHopRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=4096)
    top_k: int = 5
    max_hops: int = 3


class AgenticResponse(BaseModel):
    original_query: str
    strategy: str
    answer: str
    reflections: list[ReflectionStep] = []
    retrieved_docs: list[Document] = []
    timing_ms: float = 0.0
    citations: list[str] = []


class HealthResponse(BaseModel):
    status: str
    strategies: list[str]
    corpus_size: int
    corpus_categories: list[str]
    web_corpus_size: int
