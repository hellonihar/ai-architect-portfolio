from pydantic import BaseModel, Field


class RefineRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=4096)
    strategy: str | None = None
    conversation_history: list[str] | None = None


class RefineResponse(BaseModel):
    original_query: str
    refined_queries: list[str]
    strategy: str
    explanation: str | None = None
    metadata: dict = {}


class AutoRefineRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=4096)
    conversation_history: list[str] | None = None


class EvaluateRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=4096)
    strategy: str | None = None
    conversation_history: list[str] | None = None


class EvaluationScore(BaseModel):
    criterion: str
    raw_score: int
    refined_score: int
    explanation: str


class EvaluateResponse(BaseModel):
    original_query: str
    raw_queries: list[str]
    refined_queries: list[str]
    strategy: str
    scores: list[EvaluationScore]
