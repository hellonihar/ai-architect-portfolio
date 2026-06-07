import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.schemas import (
    AutoRefineRequest,
    EvaluateRequest,
    EvaluateResponse,
    RefineRequest,
    RefineResponse,
)
from refinery.engine import RefineryEngine

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="L1 Query Refinery",
    description="Pre-retrieval optimization strategies: query rewriting, HyDE, multi-query, query decomposition",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = RefineryEngine()


@app.post("/refine", response_model=RefineResponse)
async def refine(req: RefineRequest):
    return engine.refine(
        query=req.query,
        strategy=req.strategy,
        conversation_history=req.conversation_history,
    )


@app.post("/auto-refine", response_model=RefineResponse)
async def auto_refine(req: AutoRefineRequest):
    return engine.auto_refine(
        query=req.query,
        conversation_history=req.conversation_history,
    )


@app.post("/evaluate", response_model=EvaluateResponse)
async def evaluate(req: EvaluateRequest):
    return engine.evaluate(
        query=req.query,
        strategy=req.strategy,
        conversation_history=req.conversation_history,
    )


@app.get("/health")
async def health():
    return {"status": "healthy", "strategies": list(engine.strategies.keys())}
