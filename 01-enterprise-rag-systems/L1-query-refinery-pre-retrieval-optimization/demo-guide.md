# Demo Guide — L1 Query Refinery (Pre-Retrieval Optimization)

How to present this project to an audience — portfolio review, interview, or stakeholder walkthrough.

---

## Setup

```bash
cd 01-enterprise-rag-systems/L1-query-refinery-pre-retrieval-optimization
cp .env.example .env
# Set GROQ_API_KEY in .env for LLM-powered features
docker compose up --build
```

Backend at `http://localhost:8000`, Frontend at `http://localhost:8501`.

To run without Docker:

```bash
# Terminal 1: Backend (cd into backend/ for import resolution)
cd backend
uv run uvicorn api.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

---

## Demo Flow (10–12 min)

### 1. Context — why pre-retrieval? (1 min)

Open the README or the architecture diagram. Say:

> "In a standard RAG pipeline, the user's raw query goes straight to the retriever. But users type ambiguous, context-dependent, or compound queries all the time. Garbage in → garbage out.
>
> L1 sits upstream of retrieval. It takes the raw query and transforms it into one or more well-formed search queries. This is a cheap intervention that dramatically improves retrieval quality."

Open `http://localhost:8501` in the browser.

---

### 2. Query Rewriter — resolving ambiguity (2 min)

**Query:** `"what about the results"` with conversation history `"How did Q3 go?"`

**Narrative:**

> "Query Rewriter resolves ambiguity — pronouns, vague references, incomplete sentences — using optional conversation history."

**What to show:**
- Enter the query and conversation history
- Select `query_rewriter` strategy
- Click "Refine"
- Show the refined query: `"What were the Q3 2025 financial results?"`
- Point out that `"the results"` → `"Q3 2025 financial results"` using history context

**Try also:**
| Raw Query | History | What Happens |
|---|---|---|
| `"is it secure"` | `"What about our new auth service?"` | Resolves "it" → "auth service" |
| `"explain that thing from earlier"` | (empty) | Rephrases for clarity without context |

**Why this matters:** Real users don't write perfect search queries. This is the first line of defense.

---

### 3. HyDE — hypothetical document embedding (2 min)

**Query:** `"Explain how Kafka achieves exactly-once semantics in stream processing"`

**Narrative:**

> "HyDE generates a hypothetical ideal document that would answer the query, then embeds that document for vector search. The intuition: similar queries don't always embed near each other, but a query and its ideal answer do.
>
> Instead of searching with the query embedding, HyDE searches with the embedding of a document that *would* be the perfect answer. This often finds better results."

**What to show:**
- Enter the query
- Select `hyde` strategy
- Click "Refine"
- Show the hypothetical document generated (in the metadata expander)
- Note that the refined query is the full hypothetical document, not a short rewrite

**Why this matters:** HyDE shifts retrieval from "find documents matching these words" to "find documents that would answer this question" — a fundamentally different and often better approach.

---

### 4. Multi-Query — search diversity (2 min)

**Query:** `"What are the latest trends in machine learning?"`

**Narrative:**

> "Multi-Query expands a single query into multiple variants, each emphasizing a different angle. These are searched in parallel and the results are deduplicated. This casts a wider net and increases recall."

**What to show:**
- Enter the query
- Select `multi_query` strategy
- Click "Refine"
- Show the 3–5 generated variants, e.g.:
  - `"Recent advances in machine learning"`
  - `"State-of-the-art ML trends 2025"`
  - `"Emerging topics in AI and deep learning"`
  - `"What's new in machine learning research currently"`

**Why this matters:** A single query might miss relevant documents due to vocabulary mismatch. Multi-query mitigates this by searching from multiple lexical angles.

---

### 5. Query Decomposer — splitting compounds (2 min)

**Query:** `"What are the ACID properties in databases and how does the CAP theorem relate to them?"`

**Narrative:**

> "Compound questions with 'and' or 'also' are actually multiple queries. If you search for the whole thing, neither part gets full attention. Decomposition splits them into atomic sub-queries, each searched independently."

**What to show:**
- Enter the query
- Select `query_decomposer` strategy
- Click "Refine"
- Show the sub-queries:
  - `"What are the ACID properties in databases?"`
  - `"How does the CAP theorem relate to ACID properties?"`
- Note that the second sub-query is context-aware — it connects back to the first part

**Try also:** `"What is event sourcing and how does it relate to CQRS and log compaction?"`

**Why this matters:** Compound queries are common in enterprise settings. Decomposition ensures each atomic question gets proper retrieval.

---

### 6. Auto-Classify — let the LLM decide (1 min)

**Query:** `"they said it would work but how can I verify that"`

**Narrative:**

> "Auto-Classify uses the LLM to pick the best strategy automatically. It analyzes the query and routes it to the most appropriate refiner."

**What to show:**
- Select `auto` strategy
- Click "Refine"
- Show the selected strategy and explanation
- For this query, it should pick `query_rewriter` (ambiguous, pronouns)
- The response shows which strategy was chosen and why

---

### 7. Evaluation Tab — measuring improvement (2 min)

**Query:** `"what about the results"` with strategy `query_rewriter`

**Narrative:**

> "The Evaluate endpoint scores both the raw and refined query on three axes: Clarity, Specificity, and Search-readiness. This quantifies the improvement."

**What to show:**
- Switch to the "Evaluate" tab
- Enter the query and select `query_rewriter`
- Click "Evaluate"
- Show the three metric cards:
  - **Clarity:** raw 3 → refined 9 (delta +6)
  - **Specificity:** raw 2 → refined 8 (delta +6)
  - **Search-readiness:** raw 4 → refined 9 (delta +5)
- Hover to show the explanation for each score

---

## Sample Queries Reference

| Strategy | Best Query | Why It Works |
|---|---|---|
| **Query Rewriter** | `"how does it compare"` + history `"Compare Kafka and Pulsar"` | Resolves "it" using context |
| **HyDE** | `"Explain the transformer architecture in NLP"` | Factual/descriptive — HyDE writes a mini-article |
| **Multi-Query** | `"Best practices for microservices deployment"` | Broad topic with multiple angles |
| **Query Decomposer** | `"What is RAG and how does it relate to vector databases?"` | Contains two distinct questions |
| **Auto** | `"they said it would work but how can I verify"` | Ambiguous — routes to query_rewriter |

---

## What to Emphasize Per Audience

| Audience | Key Message | Best Demo |
|---|---|---|
| **Technical interview** | Strategy architecture (base classes), LLM integration, evaluation methodology | Evaluate tab + strategy code structure |
| **Engineering manager** | Zero external dependencies, easy integration via HTTP, meaningful quality metrics | Multi-Query breadth + Evaluate scores |
| **Portfolio review** | Understanding that RAG quality starts before retrieval, progression from L0→L1 | Show L0 fetches raw → L1 refines first |
| **Stakeholder** | Cost-effective improvement — an LLM call is cheaper than bad retrieval | Query Rewriter with history context |

---

## Interview Talking Points

**"Why improve queries before retrieval instead of after?"**
> Pre-retrieval is cheap — one LLM call transforms the query before any embedding or search cost. Post-retrieval fixes (reranking, compression) operate on results you already paid to retrieve. Getting the query right first reduces downstream waste.

**"When would you use HyDE vs. Multi-Query?"**
> HyDE works best for factual/descriptive queries where the ideal answer has a known structure. Multi-Query is better for exploratory queries where you want coverage across subtopics. They're complementary — you could run both and fuse results.

**"How would you extend this?"**
> Add a query expansion step (add synonyms or related terms), integrate with a cache of common query transformations, or add a step that detects query intent (navigational/informational/transactional) before routing.

**"What's the next level?"**
> L1 improves the query. L2 improves the retrieved results (reranking, compression). L3 adds hybrid retrieval signals. L4 makes the LLM the controller of the entire loop. Each level builds on the previous.
