# Demo Guide — L3 Hybrid & Multi-Route Retrieval

How to present this project to an audience.

---

## Setup

```bash
cd 01-enterprise-rag-systems/L3-hybrid-multi-route-retrieval
cp .env.example .env
# Set GROQ_API_KEY for LLM-based query routing (optional — falls back to embedding similarity)
docker compose up --build
```

Backend at `http://localhost:8002`, Frontend at `http://localhost:8503`.

To run without Docker:

```bash
uv venv --python 3.12
uv sync
uv run python main.py                                 # Terminal 1: backend

cd frontend
pip install -r requirements.txt
streamlit run app.py --server.port=8503                # Terminal 2: frontend
```

---

## Demo Flow (12–15 min)

### 1. Context — why multiple retrievers? (1 min)

Open the README architecture diagram. Say:

> "L1 and L2 optimize a single retrieval path — better queries, better results. But some queries need different retrieval strategies. A keyword lookup ('CAP theorem') wants BM25. A conceptual question ('Compare REST and gRPC') wants semantic search. A relational query ('Which databases work with LangChain?') wants graph traversal.
>
> L3 combines all three — dense (semantic), sparse (keyword), graph (entity-relationship) — with intelligent routing and configurable fusion."

Open `http://localhost:8503` in the browser.

---

### 2. Sparse Retrieval (BM25) — precision keyword search (2 min)

**Query:** `"What is the CAP theorem?"`

**Narrative:**

> "BM25 is the modern version of TF-IDF. It ranks documents by keyword overlap with the query, with term frequency saturation and document length normalization. For factual queries with specific terminology, it's hard to beat."

**What to show:**
- Stay in the "Search" tab
- Select `sparse` retriever, fusion `none`, top_k=10
- Click "Search"
- Show that the top results contain exact matches of "CAP theorem" — precise and relevant
- The scoring is based on lexical overlap, not semantics

**Try also:** `"ACID properties"`, `"B-tree index"` — queries with specific technical terms.

**Why this matters:** Dense retrieval can miss rare terms. Sparse retrieval guarantees exact-match recall.

---

### 3. Dense Retrieval (BGE) — semantic understanding (2 min)

**Query:** `"Compare REST and gRPC communication styles"`

**Narrative:**

> "Dense retrieval uses sentence-transformer embeddings (BGE-small-v1.5) to represent both query and documents as vectors in a 384-dimensional space. It finds documents whose meaning is closest to the query, even if they share no exact keywords."

**What to show:**
- Select `dense` retriever, fusion `none`
- Click "Search"
- Show that results mention REST and gRPC concepts even if the exact phrase isn't present
- Note that semantic search captures the *concept* of comparison and communication styles

**Why this matters:** Users don't always know the right keywords. Semantic search bridges vocabulary gaps.

---

### 4. Graph Retrieval (NetworkX) — entity relationships (2 min)

**Query:** `"Which databases work with LangChain?"`

**Narrative:**

> "The graph retriever builds a NetworkX graph from the corpus — 105 nodes (documents + entity concepts) and 422 edges (document-entity mentions + same-category relationships). For queries about relationships between entities, graph traversal finds connections that vector search can't."

**What to show:**
- Select `graph` retriever, fusion `none`
- Click "Search"
- Show that results connect LangChain → databases → specific DB types
- Point out that these connections come from entity relationships in the graph, not text similarity

**Try also:** `"What is the relationship between attention and transformers?"` — shows the entity chain: attention → self-attention → transformer.

**Why this matters:** Relational queries ("What X connects to Y?") are the hardest for pure vector search. Graph retrieval solves this naturally.

---

### 5. Hybrid + Fusion — combining signals (2 min)

**Query:** `"Explain how vector databases enable semantic search"`

**Narrative:**

> "Hybrid retrieval combines dense and sparse results using configurable fusion strategies. This gives you the best of both worlds — semantic understanding from dense, exact-match precision from sparse."

**What to show:**
- Select `hybrid` retriever, try each fusion method:

| Fusion | Alpha | Behavior |
|---|---|---|
| `rrf` | — | Reciprocal Rank Fusion — balanced, rank-based |
| `weighted` | 0.7 | Emphasizes dense (semantic) more |
| `weighted` | 0.3 | Emphasizes sparse (keyword) more |
| `contextual` | auto | Adaptive alpha per query |

- Show the same query with RRF vs weighted(0.7) vs weighted(0.3)
- Note how the result ordering changes

**Why this matters:** Different queries need different fusion balances. RRF is safe and general; weighted gives you control; contextual adapts automatically.

---

### 6. Auto-Route — LLM chooses the strategy (2 min)

**Query:** `"What is the relationship between attention mechanisms and the Transformer architecture?"`

**Narrative:**

> "Auto-Route classifies the query into one of four types — factual, semantic, exploratory, or relational — using an LLM (Groq/Qwen) with embedding similarity fallback. It then selects the optimal retriever + fusion combination for that type."

**What to show:**
- Switch to the "Auto-Route" tab
- Enter the query, click "Auto-Route"
- Show the Route Decision card:
  - **Query Type:** `relational` (because it asks about relationships)
  - **Confidence:** 0.85+
  - **Retrievers:** `["graph", "dense"]`
  - **Fusion:** `rrf`
  - **Explanation:** "Relational query detected — routing to graph + dense with RRF fusion"
- Show the results below

**Try each query type:**

| Query | Expected Type | Route |
|---|---|---|
| `"What is the CAP theorem?"` | factual | Sparse + Dense → RRF |
| `"Compare REST and gRPC"` | semantic | Dense + Sparse → Weighted |
| `"What are the latest trends in LLM research?"` | exploratory | Dense → RRF |
| `"Which databases work with LangChain?"` | relational | Graph + Dense → RRF |

**Why this matters:** No single retriever is best for all queries. Routing matches the query to the right tool. This is the foundation of L4's agentic approach.

---

### 7. Compare All — side-by-side retriever comparison (2 min)

**Query:** `"What is the relationship between attention and transformers?"`

**Narrative:**

> "The Compare tab runs all four retrievers on the same query and shows the results side-by-side. This makes the differences in retrieval strategy visible."

**What to show:**
- Switch to "Compare All" tab
- Enter the query, click "Compare All"
- Show the metric row: each retriever's result count
- Click through each tab:
  - **Dense:** semantic matches on "attention" and "transformer" as concepts
  - **Sparse:** exact matches on those words
  - **Graph:** entity-relationship paths connecting them
  - **Hybrid:** combined results from both dense and sparse

---

## Sample Queries Reference

| Tab | Best Query | Why It Works |
|---|---|---|
| **Search (dense)** | `"Compare REST and gRPC communication styles"` | Semantic similarity, no exact phrase needed |
| **Search (sparse)** | `"What is the CAP theorem?"` | Exact terminology |
| **Search (graph)** | `"Which databases work with LangChain?"` | Entity-relationship traversal |
| **Search (hybrid + RRF)** | `"Explain how vector databases enable semantic search"` | Combines semantic + keyword |
| **Auto-Route** | `"What is the relationship between attention and transformers?"` | Relational → graph+dense |
| **Compare All** | `"What is the relationship between attention and transformers?"` | See all 4 strategies |

---

## What to Emphasize Per Audience

| Audience | Key Message | Best Demo |
|---|---|---|
| **Technical interview** | Graph construction, fusion math (RRF formula), classifier fallback chain | Auto-Route decision card + RRF vs weighted comparison |
| **Engineering manager** | No external deps, graceful LLM fallback, modular retriever architecture | Run without API key — falls back to embedding classifier |
| **Portfolio review** | This is the retrieval foundation that L4 builds on for agentic control | Show Auto-Route → show L4 how it adds reflection |
| **Stakeholder** | One-size retrieval doesn't fit all — routing selects the right tool per query | Compare All — four strategies, same query, different results |

---

## Interview Talking Points

**"Why not just use hybrid for everything?"**
> Hybrid helps but isn't optimal for every case. Graph retrieval captures entity relationships that hybrid (dense+sparse) misses entirely. And routing means you don't pay the cost of running all retrievers on every query — graph traversal is expensive.

**"How does the classifier work without an LLM?"**
> The embedding classifier embeds the query and compares it to prototype embeddings for each query type (factual, semantic, exploratory, relational) using cosine similarity. It picks the closest match. Less accurate than the LLM classifier, but works without any API key.

**"What's the RRF formula?"**
> RRF = sum of 1/(k + rank_i) for each result list. k=60 is the default. It's rank-based, not score-based, so it works across retrievers with incomparable score distributions. Simple, robust, and effective.

**"How does this connect to L4?"**
> L4 takes the routing concept further — instead of routing to a retriever, it routes to an *agentic strategy* (Self-RAG, CRAG, etc.). The L3 router picks a retrieval tool. The L4 agent decides whether to retrieve at all, evaluates quality, and loops until satisfied.
