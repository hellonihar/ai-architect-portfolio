# Demo Guide — L4 Agentic / Self-Guided RAG

How to present this project to an audience (portfolio review, interview, or stakeholder walkthrough).

---

## Setup

```bash
cd 01-enterprise-rag-systems/L4-agentic-self-guided-rag
# Set your API key
$env:GROQ_API_KEY="gsk_..."
uv run python main.py              # Terminal 1: backend at :8003

# Frontend (Terminal 2):
cd frontend
pip install -r requirements.txt
streamlit run app.py                # Frontend at :8501
```

**Tip:** Set `GROQ_API_KEY` before starting so the LLM is live — responses will be substantively better than the fallback mode.

---

## Demo Flow (15–20 min)

### 1. Context — what is L4? (2 min)

Open the project README or the architecture section. Say:

> "L0–L3 covered the retrieval pipeline: naive RAG, query refinement, result refinement, and hybrid multi-route retrieval. At each level, retrieval decisions were static — the LLM was a consumer of retrieved context.
>
> L4 flips this: **the LLM becomes the controller**. It decides whether to retrieve, evaluates quality, rewrites queries, decomposes complex questions, and reflects on its own outputs. This is the difference between a pipeline and an agent."

Open `http://localhost:8501` in the browser.

---

### 2. Self-RAG Tab — the foundation (3 min)

**Query:** `"What is CQRS and how does it relate to event sourcing?"`

**Narrative:**

> "Self-RAG is the most direct agentic pattern. The LLM makes three decisions:
> 1. **Should I retrieve?** — It decides whether external knowledge is needed.
> 2. **Are these passages relevant?** — It filters retrieved results using reflection tokens.
> 3. **Is my answer supported by sources?** — It verifies citations before responding."

**What to show:**
- Click "Run Self-RAG"
- Scroll to the **Reflection Trace** expander
- Point out each step: `retrieve_decision` → `retrieve` → `reflect_relevance` (x10) → `generate` → `reflect_citation` (x10)
- Show that irrelevant/noise docs were filtered out (look for `irrelevant` labels)
- Show the final answer with citations

**Why this matters:** Without Self-RAG, all retrieved documents are fed to the LLM regardless of quality. Self-RAG gates what goes in.

---

### 3. CRAG Tab — handling bad retrieval (3 min)

**Query:** `"What is the Roman Empire's view on stream processing?"`

This query is intentionally odd — it combines a noise topic (Roman Empire) with a technical concept. It should produce low-quality retrieval.

**Narrative:**

> "CRAG adds a quality gate. After retrieval, it asks the LLM: 'How well do these passages answer the query?' If quality is low, the system takes corrective action."

**What to show:**
- Click "Run CRAG"
- Show the Reflection Trace: `score_quality` shows `low` quality
- It may fall back to the web corpus or LLM knowledge
- Show the `fallback` step entry
- Compare with the same query in Self-RAG (which won't correct poor results)

**Alternative cleaner demo:** Use `"How does consistent hashing work in distributed databases?"` — retrieval will be high quality, so CRAG passes through. Then show the trace with `quality: high` and no correction needed.

**Why this matters:** Real-world RAG systems frequently retrieve garbage. CRAG prevents garbage-in-garbage-out.

---

### 4. Adaptive RAG Tab — smart routing (3 min)

Try three queries of increasing complexity:

| Query | Expected Classification | What Happens |
|---|---|---|
| `"What is 2+2?"` | simple | Direct LLM, no retrieval. Fastest response. |
| `"Explain the CAP theorem."` | moderate | Single Self-RAG pass. |
| `"How do Kafka transactions achieve exactly-once semantics in stream processing?"` | complex | Routes to Multi-hop. Multiple sub-questions. |

**Narrative:**

> "Not all queries need the same treatment. Adaptive RAG classifies complexity and routes accordingly. Simple questions skip retrieval entirely — reducing latency and cost. Complex questions get the full agentic treatment."

**What to show:**
- Run each query in the Adaptive tab
- Show the Reflection Trace: first step is `complexity_classification` with the decision
- Note the timing difference: simple (~100ms), moderate (~2-3s), complex (~5-8s)

**Why this matters:** Production systems handle a mix of query types. Adaptive routing optimizes cost, latency, and accuracy simultaneously.

---

### 5. Multi-hop Tab — connecting the dots (3 min)

**Query:** `"How do Kafka transactions achieve exactly-once semantics in stream processing?"`

**Narrative:**

> "Some questions can't be answered from a single document. They require connecting information across multiple sources. Multi-hop decomposes the question into sub-questions, answers each one with retrieval, reflects on completeness, and synthesizes the final answer."

**What to show:**
- Click "Run Multi-hop" with max_hops=3
- Show the Reflection Trace:
  - `decompose` — shows the sub-questions generated
  - `retrieve` (hop 1) + `reflect_completeness` (hop 1)
  - `retrieve` (hop 2) + `reflect_completeness` (hop 2)
  - `synthesize` — combines sub-answers
- Point out that each hop retrieved from different documents (ds-01, ds-03, ds-02 — following the entity chain Kafka → exactly-once → stream processing)

**Why this matters:** Multi-hop is how you answer real-world questions that span documents — competitor analysis, root-cause investigations, research synthesis.

---

### 6. Auto Tab — let the LLM decide (2 min)

**Query:** `"What is the difference between model drift and concept drift?"`

**Narrative:**

> "The Auto strategy lets the LLM pick the best strategy for the query. It's a meta-agent — it reasons about which agentic pattern to use and delegates accordingly."

**What to show:**
- Click "Run Auto"
- Show the Reflection Trace: `strategy_selection` at the top shows which was chosen

**Why this matters:** This is the highest level of abstraction — the system self-configures per query.

---

### 7. Trace Explorer Tab — full comparison (3 min)

**Narrative:**

> "The Trace Explorer runs all strategies side-by-side so you can compare their approaches."

**What to show:**
- Click "Run All Strategies"
- The tab renders each strategy's answer in its own sub-tab
- Scroll through and compare:
  - **Answers** — do they agree? Which is more thorough?
  - **Reflection traces** — how many steps did each take?
  - **Retrieved documents** — did different strategies find different docs?

**Why this matters:** In production you'd A/B test strategies. This tab visualizes the trade-offs.

---

## Sample Queries Reference

### Best for Self-RAG
- `"What is CQRS and how does it relate to event sourcing?"`
- `"Explain the relationship between dense retrieval and semantic search."`

### Best for CRAG
- `"What is the Roman Empire's view on stream processing?"` (triggers fallback)
- `"How does vector database embedding enable semantic search?"` (clean pass-through)

### Best for Adaptive
- Simple: `"What is 2+2?"`
- Moderate: `"Explain how the bagel theorem works."` (outside corpus → LLM knowledge)
- Complex: `"How do ACID properties and the CAP theorem influence distributed transaction design?"`

### Best for Multi-hop (these require entity chains)
- `"How do Kafka transactions achieve exactly-once semantics in stream processing?"`
- `"Why is cross-validation important for detecting data leakage during hyperparameter tuning?"`
- `"How do microservices use circuit breakers to improve observability through distributed tracing?"`

### Best for Auto
- Let the audience pick any query. Auto routes it.

---

## What to Emphasize Per Audience

| Audience | Key Message | Best Demo |
|---|---|---|
| **Technical interview** | Depth of architecture, extensibility via base classes, testing patterns | Trace Explorer + code structure |
| **Engineering manager** | Production readiness, error handling, graceful degradation without API key | CRAG fallback + Adaptive latency |
| **Portfolio review** | Progression from L0→L4, understanding of RAG maturity model | Show L3 then L4, contrast the jump |
| **Stakeholder** | Business value: less hallucination, better answers, cost optimization | Self-RAG citations + Adaptive cost savings |

---

## Interview Talking Points

**"Why is agentic RAG better than standard RAG?"**
> Standard RAG retrieves blindly — every query triggers retrieval, every result is used. Agentic RAG reasons about whether retrieval is needed, whether results are good enough, and how to fix them if not. It's the difference between a conveyor belt and a skilled craftsman.

**"What's the main trade-off?"**
> Latency. Agentic loops make multiple LLM calls — Self-RAG might call the LLM 15+ times per query. Adaptive RAG mitigates this by routing simple queries to a fast path. In production, you'd add caching and parallelization.

**"How would you make this production-ready?"**
> Add a vector database (Pinecone/Qdrant) instead of in-memory corpus. Add caching for reflection decisions. Parallelize sub-question answering in multi-hop. Add monitoring for strategy performance per query type.

**"What's next after L4?"**
> L5 (Graph RAG) adds knowledge graph construction and traversal. L6 (Multi-modal RAG) adds image, table, and chart understanding. The agentic patterns from L4 carry forward into both.
