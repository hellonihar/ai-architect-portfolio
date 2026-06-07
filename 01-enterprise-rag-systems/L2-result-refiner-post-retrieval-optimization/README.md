# L2 Result Refiner — Post-Retrieval Optimization

Improve search results *after* retrieval and *before* generation. This service takes raw retrieved chunks and applies four post-retrieval optimization strategies — reranking, context compression, small-to-big expansion, and sliding window — with a frontend for side-by-side verification.

## Strategies

| Strategy | What It Does | Why It Matters |
|----------|-------------|----------------|
| **Reranker** | Cross-encoder (`ms-marco-MiniLM-L-6-v2`) re-scores each query-document pair, producing more accurate relevance ordering than initial vector similarity | Vector search is fast but approximate; cross-encoders are slower but significantly more precise |
| **Compressor** | LLM evaluates each chunk against the query, drops irrelevant passages, condenses redundant ones, and preserves only what matters | Reduces token waste, lowers cost, and cuts hallucination from noisy context |
| **Small-to-Big** | Retrieve precise child chunks (sentences), then expand to parent chunks (full sections) for richer context | Solves the precision-vs-richness tradeoff — accurate matching with complete context |
| **Sliding Window** | Dynamically select chunks based on relevance score thresholds and token budget rather than a fixed k | Adapts context size per query — broad queries get more chunks, narrow ones stay tight |

## Architecture

```
User Query
     ↓
[In-Memory Retriever] — bundled corpus of 20 AI/ML documents (6 parents, 22 child chunks)
     ↓
Raw Results (semantic similarity scores)
     ↓
[Result Refiner Engine]
    ├── Reranker         → cross-encoder scores → re-ranked with position tracking
    ├── Compressor       → LLM filters/condenses → trimmed context with token savings
    ├── Small-to-Big     → parent expansion → full document sections
    └── Sliding Window   → score threshold + token budget → optimal context window
     ↓
Response: raw vs. refined with comparison metrics
```

## Quick Start

### Local

**Backend (two options):**

```bash
# Copy and configure env (from project root)
cp .env.example .env
# Edit .env with your GROQ_API_KEY

# Run from the backend/ directory so module imports resolve correctly
cd backend

# Option A — using uv (auto-manages venv from parent dir)
uv run uvicorn api.main:app --reload --port 8001

# Option B — manual venv
..\.venv\Scripts\activate
uvicorn api.main:app --reload --port 8001
```

**Frontend (second terminal, from project root):**

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py --server.port=8502
```

### Docker

```bash
docker compose up --build
```

- Backend API: `http://localhost:8001`
- Frontend UI: `http://localhost:8502`

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/refine` | Apply a specific strategy (reranker, compressor, small_to_big, sliding_window) |
| POST | `/evaluate` | Run all 4 strategies on the same query and compare |
| GET | `/health` | Health check with strategy list and corpus size |

### `/refine` Example

```json
// Request
{ "query": "What is RAG?", "strategy": "reranker", "top_k": 10 }

// Response (simplified)
{
  "original_query": "What is RAG?",
  "strategy": "reranker",
  "raw_results": [
    { "id": "rag-1", "content": "RAG combines...", "score": 0.82 },
    { "id": "vec-1", "content": "Vector databases...", "score": 0.76 }
  ],
  "refined_results": [
    { "id": "rag-1", "content": "RAG combines...", "score": 0.91, "cross_encoder_score": 0.91 },
    { "id": "rag-2", "content": "RAG pipelines...", "score": 0.87, "cross_encoder_score": 0.87 }
  ],
  "explanation": "Re-ranked 10 documents using cross-encoder. Top 5 selected.",
  "metadata": {
    "position_changes": [
      { "id": "rag-3", "from": 5, "to": 2, "change": 3 }
    ]
  }
}
```

## Frontend

The Streamlit UI has two tabs:

| Tab | Purpose |
|-----|---------|
| **Refine** | Pick a strategy, see raw results vs. refined results side by side with position changes highlighted |
| **Compare All Strategies** | Run all 4 strategies on the same query in a single table, compare chunk counts and content quality |

## Sample Corpus

The bundled corpus contains 22 child chunks across 6 parent documents:

| Document | Chunks | Topics |
|----------|--------|--------|
| Retrieval-Augmented Generation | 4 | RAG pipeline, stages, challenges |
| Vector Databases & Embeddings | 4 | HNSW, IVF, semantic search |
| Large Language Models | 3 | GPT, Claude, Qwen, deployment |
| Prompt Engineering | 3 | Zero-shot, few-shot, chain-of-thought |
| Model Evaluation & Monitoring | 3 | Recall@k, BLEU, drift detection |
| Document Chunking Strategies | 5 | Size, overlap, semantic, small-to-big |

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError: No module named 'api'` | Running uvicorn from project root instead of `backend/` | `cd backend` then `uvicorn api.main:app` |
| `GROQ_API_KEY` not set | Missing `.env` or env var | `cp .env.example .env` and add your key |
| First request is slow | Cross-encoder model downloads on first use (~80MB) | Normal — subsequent requests are fast |
| Compressor returns errors | Groq API unavailability | Reranker, small-to-big, and sliding window work without an LLM |

## Key Design Decisions

- **Self-contained** — no external vector DB needed. Uses an in-memory retriever with BGE embeddings over a bundled sample corpus
- **Small cross-encoder** — `ms-marco-MiniLM-L-6-v2` (~80MB) keeps Docker image size reasonable while providing meaningful reranking
- **Config-only** — every setting (models, thresholds, budgets) lives in `.env`, zero hardcoded values
- **Compare-first** — the frontend is built for verification: raw vs. refined, side by side, with quantitative metrics
