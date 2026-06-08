import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from agentic.engine import AgenticEngine
from api.schemas import (
    AdaptiveRequest,
    AgenticResponse,
    HealthResponse,
    MultiHopRequest,
    SearchRequest,
)
from data.sample_corpus import get_categories
from retrieval.engine import RetrievalEngine

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="L4 Agentic / Self-Guided RAG",
    description="Self-RAG, CRAG, Adaptive RAG, and Multi-hop retrieval strategies with LLM-controlled retrieval decisions, reflection, and quality correction.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

retrieval_engine = RetrievalEngine()
agentic_engine = AgenticEngine(retrieval_engine)


@app.post("/agentic/search", response_model=AgenticResponse)
async def search(req: SearchRequest):
    try:
        return agentic_engine.search(query=req.query, top_k=req.top_k)
    except Exception as e:
        logger.exception("search failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/agentic/correct", response_model=AgenticResponse)
async def correct(req: SearchRequest):
    try:
        return agentic_engine.correct(query=req.query, top_k=req.top_k)
    except Exception as e:
        logger.exception("correct failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/agentic/adaptive", response_model=AgenticResponse)
async def adaptive(req: AdaptiveRequest):
    try:
        return agentic_engine.adaptive(
            query=req.query,
            top_k=req.top_k,
            complexity_threshold=req.complexity_threshold,
        )
    except Exception as e:
        logger.exception("adaptive failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/agentic/multihop", response_model=AgenticResponse)
async def multihop(req: MultiHopRequest):
    try:
        return agentic_engine.multihop(
            query=req.query,
            top_k=req.top_k,
            max_hops=req.max_hops,
        )
    except Exception as e:
        logger.exception("multihop failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/agentic/auto", response_model=AgenticResponse)
async def auto(req: SearchRequest):
    try:
        return agentic_engine.auto(query=req.query, top_k=req.top_k)
    except Exception as e:
        logger.exception("auto failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        status="healthy",
        strategies=agentic_engine.available_strategies + ["auto"],
        corpus_size=retrieval_engine.corpus_size,
        corpus_categories=list(get_categories().keys()),
        web_corpus_size=10,
    )
