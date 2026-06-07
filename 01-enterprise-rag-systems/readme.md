# Enterprise RAG Systems

Retrieval-augmented generation pipelines that make enterprise knowledge searchable and actionable. This category covers the full lifecycle — document ingestion, hybrid retrieval, context augmentation, LLM generation, and governance — as a modular, production-ready stack.

## RAG Levels Reference

| Level | Name | Key Techniques | Status |
|-------|------|----------------|--------|
| L0 | Naive RAG | Embed → Vector Search → Top-k → LLM | ✅ Done |
| L1 | Pre-Retrieval Optimization | Query rewriting, HyDE, multi-query, query decomposition | 🔜 Planned |
| L2 | Post-Retrieval Optimization | Reranking, context compression, small-to-big | 🔧 Partial |
| L3 | Hybrid & Multi-Route Retrieval | Sparse (BM25) + dense (vector), RRF fusion, query routing | 🔜 Planned |
| L4 | Agentic / Self-Guided RAG | Self-RAG, CRAG, Adaptive RAG, multi-hop | ❌ Not started |
| L5 | Graph RAG | Entity extraction, community detection, graph + vector hybrid | ❌ Not started |
| L6 | Multi-Modal RAG | Image/table/chart retrieval, VLM generation | ❌ Not started |

### L0 — Naive RAG
Embed → Vector search → Top-k → LLM. The current project does this (Pinecone + BGE + Qwen). One-shot, no query refinement, no retrieval improvement.

### L1 — Pre-Retrieval Optimization
Improve the query before search:
- **Query rewriting / expansion** — rephrase ambiguous queries (already have `CONDENSE_QUESTION_PROMPT` scaffold)
- **HyDE** — embed a hypothetical answer instead of the query
- **Multi-query** — N paraphrases searched in parallel, results deduplicated
- **Query decomposition** — split multi-part questions into sub-queries

### L2 — Post-Retrieval Optimization
Improve results before generation:
- **Reranking** — cross-encoder re-scores candidates (stubbed but not wired)
- **Context compression** — LLM removes irrelevant passages
- **Small-to-big** — retrieve small chunks, serve parent chunks for richness
- **Sliding window** — dynamic context sizing

### L3 — Hybrid & Multi-Route Retrieval
Multiple retrieval signals combined:
- **Sparse + dense** — BM25 + vector search fused via RRF
- **Multi-source** — SQL, knowledge graphs, APIs as additional retrievers
- **Query routing** — classify query → route to specialized index

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

