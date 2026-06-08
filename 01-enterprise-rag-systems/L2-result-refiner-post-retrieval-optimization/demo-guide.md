# Demo Guide — L2 Result Refiner (Post-Retrieval Optimization)

How to present this project to an audience.

---

## Setup

```bash
cd 01-enterprise-rag-systems/L2-result-refiner-post-retrieval-optimization
cp .env.example .env
# Set GROQ_API_KEY in .env for Compressor strategy
docker compose up --build
```

Backend at `http://localhost:8001`, Frontend at `http://localhost:8502`.

To run without Docker:

```bash
cd backend
uv run uvicorn api.main:app --reload --port 8001   # Terminal 1

cd frontend
pip install -r requirements.txt
streamlit run app.py --server.port=8502              # Terminal 2
```

---

## Demo Flow (12–15 min)

### 1. Context — why post-retrieval? (1 min)

Open the README architecture diagram. Say:

> "L1 improved the query before search. But even with a perfect query, the retriever returns a mixed bag — some relevant, some not, some too short, some too long. L2 operates on retrieved results before they reach the LLM. It re-ranks, filters, expands, and trims to build optimal context."

Open `http://localhost:8502` in the browser.

---

### 2. Reranker — precision re-ordering (3 min)

**Query:** `"What is RAG and how does it work?"`

**Narrative:**

> "The initial retrieval (cosine similarity on BGE embeddings) is fast but approximate. The reranker uses a cross-encoder (`MiniLM-L-6-v2`) that scores each query-document pair jointly — significantly more accurate but slower. We rerank the top-k retrieved chunks for optimal ordering."

**What to show:**
- Enter the query, select `reranker` strategy, top_k=10
- Click "Refine"
- Switch between **Raw Results** and **Refined** tabs
- Point out:
  - Raw results are ordered by initial similarity score
  - Refined results are re-ordered by cross-encoder score
  - Documents about RAG pipelines move up, tangential ones drop
- Expand **Metadata** to show `position_changes` — specific docs that moved up or down

**Try also:** `"What are vector databases?"` — watch chunks about HNSW/IVF rise to the top after reranking.

**Why this matters:** Cross-encoders are the gold standard for relevance ranking. This is the same technique used in production search systems at Google and Bing.

---

### 3. Compressor — LLM-powered filtering (3 min)

**Query:** `"Explain how prompt engineering techniques work"`

**Narrative:**

> "The compressor uses the LLM to evaluate each chunk against the query. It drops irrelevant passages, condenses redundant information, and preserves only what matters. This reduces token usage, lowers cost, and cuts hallucination from noisy context."

**What to show:**
- Enter the query, select `compressor` strategy
- Click "Refine"
- Show the **Raw Results** (all 10 chunks) vs **Refined** (fewer, condensed chunks)
- Note the explanation: `"Dropped X irrelevant, condensed Y redundant into Z passages"`
- Show the token savings in metadata
- Point out that noise documents about unrelated topics are filtered out entirely

**Why this matters:** LLM context windows are finite and expensive. Compression is like an editor who cuts everything that doesn't serve the answer.

---

### 4. Small-to-Big — precision + richness (2 min)

**Query:** `"What is document chunking and what strategies exist?"`

**Narrative:**

> "Small-to-Big solves the precision-vs-richness tradeoff. We retrieve small, precise chunks (sentences), then expand to their parent documents for full context. The retrieval is accurate (small chunks match precisely), but the generation has rich context (big chunks provide full meaning)."

**What to show:**
- Enter the query, select `small_to_big` strategy
- Click "Refine"
- Compare the raw results (child chunks) with refined (parent sections)
- Show that refined results are longer and more complete
- Expand metadata to see the parent-child mapping

**Why this matters:** This is the standard approach in production RAG systems (LangChain's ParentDocumentRetriever). It's simple but effective.

---

### 5. Sliding Window — dynamic context sizing (2 min)

**Query:** `"What are the main challenges in RAG systems?"`

**Narrative:**

> "Sliding Window replaces the fixed 'top-k' with dynamic context sizing. It sets a relevance threshold and a token budget, then includes chunks until either condition is met. Broad queries get more chunks; narrow ones stay tight."

**What to show:**
- Enter the query, select `sliding_window` strategy
- Click "Refine"
- Show the refined result count vs raw count
- Note the explanation: `"Selected X chunks within Y token budget at relevance threshold Z"`
- This strategy adapts — compare with `"What is RAG?"` (narrower → fewer chunks)

**Why this matters:** Fixed top-k is wasteful — simple queries get too much context, complex ones too little. Dynamic sizing optimizes for both.

---

### 6. Compare All Strategies — side-by-side (2 min)

**Query:** `"What are vector databases and how do they work?"`

**Narrative:**

> "The Compare tab runs all four strategies on the same query and shows the results side by side with chunk counts."

**What to show:**
- Switch to the "Compare All Strategies" tab
- Enter the query, click "Compare All"
- Show the metric row: raw count vs each strategy's count
  - Reranker: same count, better order
  - Compressor: fewer chunks, condensed
  - Small-to-Big: more content per chunk
  - Sliding Window: adaptive count
- Click through each strategy tab to compare results

---

## Sample Queries Reference

| Strategy | Best Query | Why It Works |
|---|---|---|
| **Reranker** | `"What is RAG and how does it work?"` | Cross-encoder pushes RAG-specific chunks to top |
| **Compressor** | `"Explain how prompt engineering techniques work"` | LLM filters out non-prompt chunks, keeps relevant ones |
| **Small-to-Big** | `"What is document chunking and what strategies exist?"` | 5 child chunks exist on this topic → expanded to parents |
| **Sliding Window** | `"What are the main challenges in RAG systems?"` | Dynamic threshold adapts to available relevant content |
| **Compare All** | `"What are vector databases and how do they work?"` | See all 4 strategies on one query |

---

## What to Emphasize Per Audience

| Audience | Key Message | Best Demo |
|---|---|---|
| **Technical interview** | Cross-encoder architecture, LLM-as-filter tradeoffs, dynamic thresholding | Reranker metadata (position_changes) + Compressor token savings |
| **Engineering manager** | No external deps, measurable improvements, graceful degradation without LLM | Show Compressor needs API key but other 3 work without it |
| **Portfolio review** | This is the optimization layer that makes L0 production-ready | Compare All — raw vs all 4 strategies |
| **Stakeholder** | Better answers with less hallucination, lower cost per query | Compressor token reduction + Reranker precision gains |

---

## Interview Talking Points

**"How does a cross-encoder differ from a bi-encoder?"**
> A bi-encoder (like BGE) encodes query and document independently into vectors, then uses cosine similarity — fast but loses cross-attention. A cross-encoder processes query and document jointly through the same transformer, producing a much more accurate relevance score. Tradeoff: cross-encoders are O(n) per document pair and can't pre-compute embeddings.

**"When would you skip the compressor?"**
> The compressor adds an LLM call, which adds latency and cost. For latency-sensitive applications, the reranker alone may suffice. The compressor is most valuable when context windows are tight or retrieval quality is noisy.

**"How would you extend this?"**
> Add a query-aware summary step (extractive then abstractive), integrate with a real vector DB, add an ensemble reranker that combines multiple cross-encoders, or add a cache for frequent query patterns.

**"What does L3 add beyond L2?"**
> L2 optimizes results from a single retriever. L3 adds multiple retrieval signals (sparse, dense, graph) with routing and fusion. L2 is about making one source better; L3 is about knowing which source to use.
