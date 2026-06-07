from pydantic import BaseModel, Field


class Document(BaseModel):
    id: str
    content: str
    score: float
    route: str = ""
    metadata: dict = {}


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=4096)
    retriever: str = "hybrid"
    fusion_method: str = ""
    top_k: int = 10
    alpha: float = 0.5


class RouteDecision(BaseModel):
    query: str
    classified_type: str
    confidence: float
    selected_retrievers: list[str]
    fusion_method: str
    explanation: str


class SearchResponse(BaseModel):
    original_query: str
    retriever: str
    fusion_method: str
    results: list[Document]
    route_decision: RouteDecision | None = None
    timing_ms: float = 0.0


class CompareResponse(BaseModel):
    original_query: str
    strategies: dict[str, list[Document]]


class HealthResponse(BaseModel):
    status: str
    retrievers: list[str]
    fusion_methods: list[str]
    corpus_size: int
    graph_nodes: int
    graph_edges: int
