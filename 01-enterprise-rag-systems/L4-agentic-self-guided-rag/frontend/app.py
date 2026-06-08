import json
import os
import time

import requests
import streamlit as st

API_BASE = os.environ.get("API_BASE", "http://localhost:8003")


def api_post(endpoint: str, payload: dict) -> dict | None:
    try:
        resp = requests.post(f"{API_BASE}{endpoint}", json=payload, timeout=120)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"API error: {e}")
        return None


def api_get(endpoint: str) -> dict | None:
    try:
        resp = requests.get(f"{API_BASE}{endpoint}", timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"API error: {e}")
        return None


st.set_page_config(page_title="L4 — Agentic / Self-Guided RAG", layout="wide")
st.title("L4 — Agentic / Self-Guided RAG")
st.markdown(
    "LLM-controlled retrieval with reflection, quality correction, adaptive routing, and multi-hop decomposition."
)

health = api_get("/health")
if health:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Strategies", ", ".join(health["strategies"]))
    col2.metric("Corpus Docs", health["corpus_size"])
    col3.metric("Categories", len(health["corpus_categories"]))
    col4.metric("Web Corpus", health["web_corpus_size"])
else:
    st.error("Backend not available. Start the API server first.")
    st.stop()

tab_search, tab_correct, tab_adaptive, tab_multihop, tab_auto, tab_trace = st.tabs(
    ["Self-RAG", "CRAG", "Adaptive RAG", "Multi-hop", "Auto", "Trace Explorer"]
)

query = st.text_input(
    "Enter your query",
    value="How do Kafka transactions achieve exactly-once semantics in stream processing?",
    key="main_query",
)
top_k = st.slider("Top-k documents", 3, 20, 10)

max_hops = 3
if tab_multihop:
    max_hops = st.slider("Max hops", 1, 5, 3, key="max_hops")

complexity_threshold = 0.7
if tab_adaptive:
    complexity_threshold = st.slider("Complexity threshold", 0.0, 1.0, 0.7, key="complexity_threshold")


def display_response(response: dict, title: str):
    if response is None:
        return

    st.subheader("Answer")
    st.markdown(response.get("answer", "No answer generated."))

    cols = st.columns(3)
    cols[0].metric("Strategy", response.get("strategy", "?"))
    cols[1].metric("Timing", f"{response.get('timing_ms', 0):.0f}ms")
    cols[2].metric("Citations", len(response.get("citations", [])))

    if response.get("citations"):
        with st.expander("Cited Documents"):
            for c in response["citations"]:
                st.code(c)

    if response.get("retrieved_docs"):
        with st.expander(f"Retrieved Documents ({len(response['retrieved_docs'])})"):
            for doc in response["retrieved_docs"]:
                st.markdown(f"**{doc['id']}** (score: {doc['score']:.3f})")
                st.text(doc["content"][:300] + "...")

    if response.get("reflections"):
        with st.expander(f"Reflection Trace ({len(response['reflections'])} steps)"):
            for i, step in enumerate(response["reflections"]):
                st.markdown(f"**Step {i+1}: {step['step_type']}** (confidence: {step['confidence']:.2f})")
                st.text(f"Input: {step['input'][:200]}")
                st.text(f"Output: {step['output'][:300]}")
                if step.get("metadata"):
                    st.json(step["metadata"])
                if i < len(response["reflections"]) - 1:
                    st.divider()


with tab_search:
    st.header("Self-RAG")
    st.markdown("LLM decides whether to retrieve, reflects on passage relevance, generates with or without passages, and verifies citations.")
    if st.button("Run Self-RAG", key="btn_search"):
        with st.spinner("Running Self-RAG..."):
            response = api_post("/agentic/search", {"query": query, "top_k": top_k})
            display_response(response, "Self-RAG")

with tab_correct:
    st.header("Corrective RAG")
    st.markdown("Retrieval quality is scored; low quality triggers query rewrite + re-retrieve or fallback to LLM/web corpus.")
    if st.button("Run CRAG", key="btn_correct"):
        with st.spinner("Running CRAG..."):
            response = api_post("/agentic/correct", {"query": query, "top_k": top_k})
            display_response(response, "CRAG")

with tab_adaptive:
    st.header("Adaptive RAG")
    st.markdown("Query complexity is classified: simple → direct LLM, moderate → Self-RAG, complex → Multi-hop.")
    if st.button("Run Adaptive RAG", key="btn_adaptive"):
        with st.spinner("Running Adaptive RAG..."):
            response = api_post("/agentic/adaptive", {
                "query": query,
                "top_k": top_k,
                "complexity_threshold": complexity_threshold,
            })
            display_response(response, "Adaptive RAG")

with tab_multihop:
    st.header("Multi-hop RAG")
    st.markdown("Query decomposed into sub-questions; each sub-question is retrieved, answered, and reflected upon before synthesis.")
    if st.button("Run Multi-hop", key="btn_multihop"):
        with st.spinner("Running Multi-hop..."):
            response = api_post("/agentic/multihop", {
                "query": query,
                "top_k": top_k,
                "max_hops": max_hops,
            })
            display_response(response, "Multi-hop")

with tab_auto:
    st.header("Auto Strategy")
    st.markdown("LLM selects the best strategy for the query.")
    if st.button("Run Auto", key="btn_auto"):
        with st.spinner("Running Auto..."):
            response = api_post("/agentic/auto", {"query": query, "top_k": top_k})
            display_response(response, "Auto")

with tab_trace:
    st.header("Trace Explorer")
    st.markdown("Compare all strategies side-by-side.")

    if st.button("Run All Strategies", key="btn_all"):
        results = {}
        with st.spinner("Running all strategies..."):
            endpoints = {
                "Self-RAG": "/agentic/search",
                "CRAG": "/agentic/correct",
                "Adaptive RAG": "/agentic/adaptive",
                "Multi-hop": "/agentic/multihop",
            }
            for name, ep in endpoints.items():
                payload = {"query": query, "top_k": top_k}
                if "adaptive" in ep:
                    payload["complexity_threshold"] = 0.7
                if "multihop" in ep:
                    payload["max_hops"] = 3
                    payload["top_k"] = 5
                results[name] = api_post(ep, payload)

        tabs = st.tabs(list(results.keys()))
        for i, (name, response) in enumerate(results.items()):
            with tabs[i]:
                if response:
                    display_response(response, name)
                else:
                    st.error(f"{name} failed")


st.markdown("---")
with st.expander("Sample Queries (click to try)"):
    sample_queries = [
        "How do Kafka transactions achieve exactly-once semantics in stream processing?",
        "How does CQRS combine with event sourcing and log compaction?",
        "Why is cross-validation important for detecting data leakage during hyperparameter tuning?",
        "How do dense retrieval and hybrid search improve RAG systems?",
        "What is the relationship between attention mechanisms and the Transformer architecture?",
        "How do ACID properties and the CAP theorem influence distributed transactions?",
        "What is a service mesh and how does it use sidecars?",
        "How does consistent hashing enable sharding in distributed databases?",
        "Explain the circuit breaker pattern in microservices.",
        "How do online learning and concept drift relate to batch inference?",
    ]
    for q in sample_queries:
        if st.button(q, key=f"sample_{q[:20]}"):
            st.session_state["main_query"] = q
            st.rerun()
