# Enterprise RAG Systems

Retrieval-augmented generation pipelines that make enterprise knowledge searchable and actionable. This category covers the full lifecycle — document ingestion, hybrid retrieval, context augmentation, LLM generation, and governance — as a modular, production-ready stack.

## RAG Levels Reference

| Level | Name | Key Techniques | Status |
|-------|------|----------------|--------|
| L0 | Naive RAG | Embed → Vector Search → Top-k → LLM | ✅ Done |
| L1 | Pre-Retrieval Optimization | Query rewriting, HyDE, multi-query, query decomposition | ✅ Done |
| L2 | Post-Retrieval Optimization | Reranking, context compression, small-to-big, sliding window | ✅ Done |
| L3 | Hybrid & Multi-Route Retrieval | Sparse (BM25) + dense (vector) + graph, RRF/weighted/contextual fusion, query routing | ✅ Done |
| L4 | Agentic / Self-Guided RAG | Self-RAG, CRAG, Adaptive RAG, multi-hop | ✅ Done |
| L5 | Graph RAG | Entity extraction, community detection, graph + vector hybrid | ❌ Not started |
| L6 | Multi-Modal RAG | Image/table/chart retrieval, VLM generation | ❌ Not started |

### L0 — Naive RAG
Embed → Vector search → Top-k → LLM. The current project does this (Pinecone + BGE + Qwen). One-shot, no query refinement, no retrieval improvement.

### L1 — Pre-Retrieval Optimization
Improve the query before search:
- **Query rewriting / expansion** — rephrase ambiguous queries using conversation history
- **HyDE** — generate a hypothetical document, embed it, search with that embedding
- **Multi-query** — N paraphrases generated and searched in parallel, results deduplicated
- **Query decomposition** — split multi-part questions into atomic sub-queries

### L2 — Post-Retrieval Optimization
Improve results before generation:
- **Reranking** — cross-encoder (`MiniLM-L-6-v2`) re-scores retrieved chunks for accurate relevance ordering
- **Context compression** — LLM filters irrelevant passages, condenses redundant ones, drops noise
- **Small-to-big** — retrieve small precise chunks, expand to parent documents for richness
- **Sliding window** — dynamic context sizing based on relevance thresholds and token budget

### L3 — Hybrid & Multi-Route Retrieval
Multiple retrieval signals combined:
- **Sparse (BM25)** — keyword-based retrieval for factual/precision queries
- **Dense (vector)** — semantic search via sentence-transformers (BGE-small)
- **Graph (entity-relationship)** — networkx graph traversal for relational queries
- **Hybrid** — sparse + dense combined with configurable fusion
- **Fusion strategies** — RRF (reciprocal rank), weighted (α-dense + (1-α)-sparse), contextual (adaptive)
- **Query routing** — LLM-based classifier with embedding fallback → maps query type (factual, semantic, exploratory, relational) to optimal retriever + fusion combination

### L4 — Agentic / Self-Guided RAG
LLM controls retrieval:
- **Self-RAG** — LLM decides when to retrieve, reflects on passages, cites
- **Corrective RAG (CRAG)** — low-quality retrieval triggers query rewrite or fallback
- **Adaptive RAG** — simple lookups vs. complex reasoning routed differently
- **Multi-hop** — iterative retrieval for sub-questions, chain results

### L5 — Graph RAG
Entity-relationship structure:
- Entity extraction + KG construction
- Community detection (Leiden) → community summaries
- Graph traversal for relational queries
- Graph + vector hybrid retrieval

### L6 — Multi-Modal RAG
Beyond text:
- Image/table/chart embedding (CLIP-like)
- Structured extraction from PDF tables
- VLM-based generation with visual context

## Projects

| Level | Project | Description | GitHub |
|-------|---------|-------------|--------|
| L0 | [Enterprise AI Copilot](./enterprise-ai-copilot) | Full-stack RAG assistant — LangChain, Pinecone, Groq (Qwen3-32b) | [View on GitHub](https://github.com/hellonihar/ai-architect-portfolio/tree/main/01-enterprise-rag-systems/enterprise-ai-copilot) |
| L1 | [Query Refinery](./L1-query-refinery-pre-retrieval-optimization) | Pre-retrieval optimization — query rewriting, HyDE, multi-query, decomposition | [View on GitHub](https://github.com/hellonihar/ai-architect-portfolio/tree/main/01-enterprise-rag-systems/L1-query-refinery-pre-retrieval-optimization) |
| L2 | [Result Refiner](./L2-result-refiner-post-retrieval-optimization) | Post-retrieval optimization — reranking, compression, small-to-big, sliding window | [View on GitHub](https://github.com/hellonihar/ai-architect-portfolio/tree/main/01-enterprise-rag-systems/L2-result-refiner-post-retrieval-optimization) |
| L3 | [Hybrid & Multi-Route Retrieval](./L3-hybrid-multi-route-retrieval) | Hybrid retrieval — sparse + dense + graph, RRF/weighted/contextual fusion, query routing | [View on GitHub](https://github.com/hellonihar/ai-architect-portfolio/tree/main/01-enterprise-rag-systems/L3-hybrid-multi-route-retrieval) |
| L4 | [Agentic / Self-Guided RAG](./L4-agentic-self-guided-rag) | Self-RAG, CRAG, Adaptive RAG, multi-hop | [View on GitHub](https://github.com/hellonihar/ai-architect-portfolio/tree/main/01-enterprise-rag-systems/L4-agentic-self-guided-rag) |

## Quick Start

```bash
# Enterprise AI Copilot (L0)
cd enterprise-ai-copilot
cp .env.example .env
docker compose up --build

# Query Refinery (L1)
cd L1-query-refinery-pre-retrieval-optimization
cp .env.example .env
docker compose up --build
```

- Copilot Backend: `http://localhost:8000`
- Copilot Frontend: `http://localhost:8501`
- Refinery API: `http://localhost:8001`
- Result Refiner API: `http://localhost:8001` | Frontend: `http://localhost:8502`

```bash
# Hybrid & Multi-Route Retrieval (L3)
cd L3-hybrid-multi-route-retrieval
cp .env.example .env
uv venv --python 3.12
uv sync
uv run python main.py

# Agentic / Self-Guided RAG (L4)
cd L4-agentic-self-guided-rag
cp .env.example .env
uv venv --python 3.12
uv sync
uv run python main.py
```

- Hybrid Retrieval API: `http://localhost:8002`
- Hybrid Retrieval Frontend: `http://localhost:8503`
- Agentic RAG API: `http://localhost:8003`
- Agentic RAG Frontend: `http://localhost:8504`
- Agentic RAG API: `http://localhost:8003`
- Agentic RAG Frontend: `http://localhost:8504`
