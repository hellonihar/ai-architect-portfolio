import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from api.schemas import (
    CompareResponse,
    HealthResponse,
    SearchRequest,
    SearchResponse,
)
from retrieval.engine import RetrievalEngine

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="L3 Hybrid & Multi-Route Retrieval",
    description="Hybrid retrieval (sparse + dense + graph) with multi-route query routing and RRF/weighted/contextual fusion",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = RetrievalEngine()


@app.post("/search", response_model=SearchResponse)
async def search(req: SearchRequest):
    try:
        docs, _, elapsed = engine.search(
            query=req.query,
            retriever_name=req.retriever,
            fusion_method=req.fusion_method,
            top_k=req.top_k,
            alpha=req.alpha,
        )
        return SearchResponse(
            original_query=req.query,
            retriever=req.retriever,
            fusion_method=req.fusion_method or engine.available_fusion[0],
            results=docs,
            timing_ms=round(elapsed, 1),
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/route", response_model=SearchResponse)
async def route_query(req: SearchRequest):
    try:
        docs, decision, elapsed = engine.route_query(
            query=req.query,
            top_k=req.top_k,
        )
        return SearchResponse(
            original_query=req.query,
            retriever="auto",
            fusion_method=decision.fusion_method if decision else "rrf",
            results=docs,
            route_decision=decision,
            timing_ms=round(elapsed, 1),
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/compare", response_model=CompareResponse)
async def compare(req: SearchRequest):
    strategies = engine.compare_all(query=req.query, top_k=req.top_k)
    return CompareResponse(
        original_query=req.query,
        strategies=strategies,
    )


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        status="healthy",
        retrievers=engine.available_retrievers,
        fusion_methods=engine.available_fusion,
        corpus_size=engine.corpus_size,
        graph_nodes=engine.graph_nodes,
        graph_edges=engine.graph_edges,
    )
