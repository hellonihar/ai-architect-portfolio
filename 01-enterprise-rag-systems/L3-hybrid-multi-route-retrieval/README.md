# L3 — Hybrid & Multi-Route Retrieval

**Level 3 in the Enterprise RAG Systems progression.** Combines sparse (BM25), dense (vector), and graph (entity-relationship) retrieval with intelligent query routing and configurable fusion strategies (RRF, weighted, contextual).

## Architecture

```
                    ┌──► DenseRetriever (sentence-transformers)
                    ├──► SparseRetriever (BM25)
Query ──► Router ──┼──► GraphRetriever (networkx entity graph)
    (LLM + embed   ├──► HybridRetriever (sparse + dense)
     fallback)     │
               Fusion Layer
          (RRF / Weighted / Contextual)
                    │
               Ranked Results
          (with route metadata + decision trace)
```

## Retrievers

| Retriever | Method | Best For |
|-----------|--------|----------|
| **Dense** | Sentence-transformer embeddings + cosine similarity | Semantic / conceptual queries |
| **Sparse** | BM25 (rank-bm25) | Keyword / factual queries |
| **Graph** | NetworkX entity-relationship graph traversal | Relational / connective queries |
| **Hybrid** | Dense + sparse combined | General purpose |

## Fusion Strategies

| Strategy | How It Works | When To Use |
|----------|--------------|-------------|
| **RRF** | Reciprocal Rank Fusion — combines rank positions across result lists | Balanced, no score normalization needed |
| **Weighted** | `α * dense_score + (1-α) * sparse_score` with min-max normalization | When you have a preference (α adjusts dense vs sparse weight) |
| **Contextual** | Same as weighted, but α is set dynamically per query via the API | Adaptive weighting per query |

## Query Routing

The router classifies queries into 4 types:

| Query Type | Example | Route |
|------------|---------|-------|
| factual | "What is the CAP theorem?" | Sparse + Dense → RRF |
| semantic | "Compare REST and gRPC" | Dense + Sparse → Weighted |
| exploratory | "What are the latest trends in LLM research?" | Dense → RRF |
| relational | "Which databases work with LangChain?" | Graph + Dense → RRF |

Classification uses **LLM (Groq/Qwen)** by default, falling back to **embedding similarity** if no API key is configured.

## API Endpoints

### `POST /search`
Run a specific retriever with a fusion strategy.

```json
{
  "query": "What is RAG and how does it relate to vector databases?",
  "retriever": "hybrid",
  "fusion_method": "rrf",
  "top_k": 10,
  "alpha": 0.5
}
```

### `POST /route`
Auto-classify the query and select the optimal route.

```json
{
  "query": "Which databases are used with LLM applications?",
  "top_k": 10
}
```

### `POST /compare`
Run all 4 retrievers in parallel for side-by-side comparison.

```json
{
  "query": "What is the relationship between attention and transformers?",
  "top_k": 5
}
```

### `GET /health`
```json
{
  "status": "healthy",
  "retrievers": ["dense", "sparse", "graph", "hybrid"],
  "fusion_methods": ["rrf", "weighted", "contextual"],
  "corpus_size": 53,
  "graph_nodes": 105,
  "graph_edges": 422
}
```

## Quick Start

### Backend

```bash
cd L3-hybrid-multi-route-retrieval
cp .env.example .env
uv venv --python 3.12
uv sync
uv run python main.py
```

Backend runs at **http://localhost:8002**

### Frontend

In a separate terminal:

```bash
cd L3-hybrid-multi-route-retrieval/frontend
pip install -r requirements.txt
streamlit run app.py
```

The frontend connects to the backend at `http://localhost:8002` by default. To use a different address, set the `API_BASE` environment variable:

```bash
# Windows PowerShell
$env:API_BASE="http://localhost:8002"; streamlit run app.py
```

Frontend runs at **http://localhost:8501**

### Docker

```bash
cd L3-hybrid-multi-route-retrieval
cp .env.example .env
docker compose up --build
```

- Backend: http://localhost:8002
- Frontend: http://localhost:8503 (port mapped by Docker Compose)

## Project Structure

```
L3-hybrid-multi-route-retrieval/
├── main.py                  # Entry point (adds backend/ to Python path, launches uvicorn)
├── pyproject.toml           # uv-managed dependencies
├── .env.example
├── docker-compose.yml
├── backend/
│   ├── api/main.py          # FastAPI: 4 endpoints
│   ├── api/schemas.py       # Pydantic models
│   ├── core/config.py       # Pydantic Settings
│   ├── data/
│   │   └── sample_corpus.py # 53 documents, 4 categories, entity annotations
│   └── retrieval/
│       ├── engine.py        # Orchestrator
│       ├── embedder.py      # BGE-small wrapper
│       ├── retrievers/      # dense, sparse, graph, hybrid
│       ├── fusion/          # rrf, weighted, contextual
│       └── routing/         # classifier (LLM + embed), router
└── frontend/
    └── app.py               # Streamlit: Search, Auto-Route, Compare tabs
```

## Sample Corpus

53 documents across 4 categories (Software Architecture, Machine Learning, LLMs, Databases & Storage) with ~80 entity annotations for graph traversal — no external API or vector database required.

Graph stats: **105 nodes** (53 documents + 52 entity concepts), **422 edges** (document-entity mentions + same-category relationships).

## Tech Stack

| Component | Technology |
|-----------|------------|
| API | FastAPI + Uvicorn |
| Embeddings | sentence-transformers (BGE-small-v1.5, 384-dim) |
| Sparse Search | rank-bm25 |
| Graph | networkx |
| Routing | LangChain Groq (optional) + embedding similarity fallback |
| Fusion | RRF, weighted min-max, contextual adaptive |
| Frontend | Streamlit |
| Package | uv / pip |
