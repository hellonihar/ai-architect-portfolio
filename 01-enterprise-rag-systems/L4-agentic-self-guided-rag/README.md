# L4 — Agentic / Self-Guided RAG

**Level 4 in the Enterprise RAG Systems progression.** LLM-controlled retrieval with four agentic strategies: Self-RAG, Corrective RAG (CRAG), Adaptive RAG, and Multi-hop RAG.

## Architecture

```
                     ┌── Self-RAG ──────────────┐
                     │  LLM decides to retrieve  │
                     │  → relevance reflection   │
                     │  → citation verification  │
                     │  → generate with/without  │
                     │                           │
                     ├── Corrective RAG ─────────┤
                     │  → quality scoring        │
                     │  → rewrite if medium      │
                     │  → fallback if low        │
                     │  (LLM or web corpus)      │
                     │                           │
Query ──► Router ────┼── Adaptive RAG ──────────┤
    (auto or         │  → classify complexity   │
     explicit        │  → simple: direct LLM    │
     strategy)       │  → moderate: Self-RAG    │
                     │  → complex: Multi-hop    │
                     │                           │
                     ├── Multi-hop ─────────────┤
                     │  → decompose sub-questions│
                     │  → iterative retrieval   │
                     │  → reflect completeness  │
                     │  → synthesize answers    │
                     │                           │
                     └── Auto ──────────────────┘
                        LLM selects best strategy
```

## Agentic Strategies

| Strategy | Mechanism | Best For |
|----------|-----------|----------|
| **Self-RAG** | LLM decides retrieval, reflects on relevance, verifies citations | Queries where retrieval may or may not be needed |
| **Corrective RAG** | Quality scoring → rewrite or fallback gates | Queries with uncertain retrieval quality |
| **Adaptive RAG** | Complexity classification → simple/moderate/complex path | Mixed workloads with varying complexity |
| **Multi-hop** | Sub-question decomposition + iterative retrieval + synthesis | Multi-document, relational, chain queries |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/agentic/search` | Self-RAG with reflection and citation verification |
| `POST` | `/agentic/correct` | CRAG with quality scoring, rewrite, and fallback |
| `POST` | `/agentic/adaptive` | Adaptive routing by query complexity |
| `POST` | `/agentic/multihop` | Multi-hop iterative sub-question retrieval |
| `POST` | `/agentic/auto` | LLM selects the best strategy automatically |
| `GET` | `/health` | Engine status and corpus statistics |

## Sample Corpus

~50 documents across 5 categories with:
- **Entity chains** (A→B→C): 10 cross-document chains for multi-hop queries
- **Noise documents**: 8 intentionally off-topic docs for relevance testing
- **Test queries**: 15 multi-hop queries + 15 end-to-end queries
- **Web fallback corpus**: 8 documents simulating web search results

## Quick Start

### Backend

```bash
cd L4-agentic-self-guided-rag
cp .env.example .env
# Set GROQ_API_KEY in .env for full LLM functionality
uv venv --python 3.12
uv sync
uv run python main.py
```

Backend runs at **http://localhost:8003**

### Frontend

In a separate terminal:

```bash
cd L4-agentic-self-guided-rag/frontend
pip install -r requirements.txt
streamlit run app.py
```

Frontend runs at **http://localhost:8501**

### Docker

```bash
cd L4-agentic-self-guided-rag
cp .env.example .env
docker compose up --build
```

- Backend: http://localhost:8003
- Frontend: http://localhost:8504

### Tests

```bash
cd L4-agentic-self-guided-rag
uv run pytest backend/tests/ -v
```

## Project Structure

```
L4-agentic-self-guided-rag/
├── main.py                    # Entry point (uv run python main.py)
├── pyproject.toml             # uv-managed dependencies
├── .env.example
├── docker-compose.yml
├── backend/
│   ├── api/main.py            # FastAPI: 6 endpoints
│   ├── api/schemas.py         # Pydantic models
│   ├── core/config.py         # Pydantic Settings
│   ├── data/
│   │   ├── sample_corpus.py   # ~50 documents with entity chains
│   │   └── web_fallback.py    # Simulated web corpus
│   ├── retrieval/
│   │   ├── engine.py          # Orchestrator
│   │   ├── embedder.py        # BGE-small wrapper
│   │   ├── retrievers/        # dense, sparse
│   │   └── fusion/            # rrf
│   ├── agentic/
│   │   ├── engine.py          # Agentic orchestrator
│   │   ├── llm_client.py      # Groq wrapper with structured output
│   │   ├── strategies/        # self_rag, corrective_rag, adaptive_rag, multi_hop
│   │   └── reflection/        # relevance, citation, quality checkers
│   └── tests/                 # pytest suite (api, engine, strategies)
└── frontend/
    └── app.py                 # Streamlit: 6 tabs, trace viewer
```

## Tech Stack

| Component | Technology |
|-----------|------------|
| API | FastAPI + Uvicorn |
| LLM | Groq (Qwen3-32b) via langchain-groq |
| Embeddings | sentence-transformers (BGE-small-v1.5, 384-dim) |
| Dense Search | Cosine similarity via NumPy |
| Sparse Search | rank-bm25 |
| Fusion | RRF (Reciprocal Rank Fusion) |
| Frontend | Streamlit |
| Testing | pytest + FastAPI TestClient |
| Package | uv / pip |
