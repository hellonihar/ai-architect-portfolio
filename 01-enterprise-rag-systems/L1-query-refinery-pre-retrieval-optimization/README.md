# L1 Query Refinery — Pre-Retrieval Optimization

Improve search queries *before* they hit the retriever. This service sits upstream of any RAG pipeline, transforming raw user input into better search queries using four strategies — plus an auto-classifier that picks the right one.

## Strategies

| Strategy | What It Does | When To Use |
|----------|-------------|-------------|
| **Query Rewriter** | Rephrases ambiguous, poorly-formed, or context-dependent queries for clarity | "What about the Q3 report?" → "Show me the Q3 2025 financial report" |
| **HyDE** (Hypothetical Document Embeddings) | Generates a hypothetical ideal document, then embeds it for vector search | Factual or descriptive queries where similar wording matters |
| **Multi-Query** | Expands one query into N variants searched in parallel | Broad topics that benefit from multiple search angles |
| **Query Decomposer** | Splits compound questions into atomic sub-queries | "What are Q3 sales and who leads the engineering team?" → two separate queries |

## Architecture

```
Raw Query → [Refinery Engine]
                ├── Auto-Classify → [LLM picks strategy]
                ├── Query Rewriter → Refined text
                ├── HyDE           → Hypothetical doc + embedding
                ├── Multi-Query    → N query variants
                └── Query Decomposer → Sub-queries
                         ↓
                Response with refined queries + metadata
```

## Quick Start

```bash
cp .env.example .env
# Edit .env with your Groq API key
docker compose up --build
```

Backend API: `http://localhost:8000`

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/refine` | Apply a specific strategy |
| POST | `/auto-refine` | Auto-detect best strategy via LLM |
| POST | `/evaluate` | Compare raw vs. refined with quality scores |
| GET | `/health` | Health check |

### `/refine` Example

```json
// Request
{ "query": "what about the results", "strategy": "query_rewriter", "conversation_history": ["How did Q3 go?"] }

// Response
{
  "original_query": "what about the results",
  "refined_queries": ["What were the Q3 2025 financial results?"],
  "strategy": "query_rewriter",
  "explanation": "Rewritten using conversation history for context resolution"
}
```

## Integration

This service is fully independent — no shared dependencies with the main RAG pipeline. It communicates via HTTP. To integrate into any RAG pipeline, call `/refine` with the raw query and feed the refined query(s) into the retriever.
