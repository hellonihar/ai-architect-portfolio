import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.schemas import RefineRequest, RefineResponse, EvaluateResponse
from refiner.engine import RefinerEngine

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="L2 Result Refiner",
    description="Post-retrieval optimization: cross-encoder reranking, context compression, small-to-big expansion, sliding window",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = RefinerEngine()


@app.post("/refine", response_model=RefineResponse)
async def refine(req: RefineRequest):
    return engine.refine(query=req.query, strategy=req.strategy, top_k=req.top_k)


@app.post("/evaluate", response_model=EvaluateResponse)
async def evaluate(req: RefineRequest):
    return engine.evaluate(query=req.query, top_k=req.top_k)


@app.get("/health")
async def health():
    return {"status": "healthy", "strategies": list(engine.strategies.keys()), "corpus_size": engine.retriever.corpus_size}
