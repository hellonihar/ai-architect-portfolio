import streamlit as st
import requests
import os

API_BASE = os.getenv("API_BASE", "http://localhost:8002")

st.set_page_config(page_title="L3 Hybrid & Multi-Route Retrieval", page_icon="🔀", layout="wide")
st.title("L3 — Hybrid & Multi-Route Retrieval")
st.caption(
    "Compare dense (semantic), sparse (BM25), graph (entity-relationship), and hybrid retrieval "
    "with RRF, weighted, and contextual fusion."
)

tab_search, tab_route, tab_compare = st.tabs(["Search", "Auto-Route", "Compare All"])

# ── Tab 1: Manual Search ──────────────────────────────────────────────
with tab_search:
    col_left, col_right = st.columns([1, 1])

    with col_left:
        query = st.text_area("Query", height=100, placeholder="What is RAG and how does it relate to vector databases?")
        retriever = st.selectbox(
            "Retriever",
            ["dense", "sparse", "graph", "hybrid"],
            help="dense: semantic vector search | sparse: BM25 keyword | graph: entity-relationship | hybrid: combined dense+sparse",
        )
        fusion = st.selectbox(
            "Fusion Method",
            ["rrf", "weighted", "contextual", "none"],
            help="rrf: reciprocal rank fusion | weighted: alpha*dense+(1-alpha)*sparse | contextual: adaptive weights",
        )
        alpha = st.slider("Alpha (dense weight)", min_value=0.0, max_value=1.0, value=0.5, step=0.1,
                          help="Only used for weighted/contextual fusion")
        top_k = st.slider("Top-K", min_value=3, max_value=20, value=10)

        if st.button("Search", type="primary"):
            if query.strip():
                with st.spinner(f"Running {retriever}..."):
                    try:
                        resp = requests.post(
                            f"{API_BASE}/search",
                            json={
                                "query": query,
                                "retriever": retriever,
                                "fusion_method": fusion if fusion != "none" else "",
                                "top_k": top_k,
                                "alpha": alpha,
                            },
                            timeout=120,
                        )
                        if resp.status_code == 200:
                            st.session_state.search_result = resp.json()
                        else:
                            st.error(f"API Error: {resp.status_code} - {resp.text}")
                    except requests.exceptions.ConnectionError:
                        st.error(f"Cannot connect to backend at {API_BASE}")

    with col_right:
        if "search_result" in st.session_state:
            data = st.session_state.search_result
            st.subheader(f"Retriever: {data['retriever']}  |  Fusion: {data['fusion_method']}")
            st.caption(f"Retrieved {len(data['results'])} results in {data['timing_ms']}ms")

            for i, doc in enumerate(data["results"], 1):
                route_label = {"dense": "🔵 Dense", "sparse": "🟢 Sparse", "graph": "🟣 Graph",
                               "hybrid:dense": "🔵 Hybrid-Dense", "hybrid:sparse": "🟢 Hybrid-Sparse",
                               "hybrid:both": "🔀 Hybrid-Both"}
                badge = route_label.get(doc.get("route", ""), f"⚪ {doc.get('route', 'unknown')}")
                with st.container(border=True):
                    cols = st.columns([1, 5, 1, 1])
                    cols[0].markdown(f"**#{i}**")
                    cols[1].markdown(doc["content"][:250] + ("..." if len(doc["content"]) > 250 else ""))
                    cols[2].markdown(f"`{doc['score']:.3f}`")
                    cols[3].markdown(badge)

# ── Tab 2: Auto-Route ────────────────────────────────────────────────
with tab_route:
    col_left, col_right = st.columns([1, 1])

    with col_left:
        route_query = st.text_area("Query", height=100, key="route_query",
                                    placeholder="Which databases are commonly used with LLM applications?")
        route_top_k = st.slider("Top-K", min_value=3, max_value=20, value=10, key="route_top_k")

        if st.button("Auto-Route", type="primary", key="route_btn"):
            if route_query.strip():
                with st.spinner("Classifying and routing..."):
                    try:
                        resp = requests.post(
                            f"{API_BASE}/route",
                            json={"query": route_query, "top_k": route_top_k},
                            timeout=120,
                        )
                        if resp.status_code == 200:
                            st.session_state.route_result = resp.json()
                        else:
                            st.error(f"API Error: {resp.status_code} - {resp.text}")
                    except requests.exceptions.ConnectionError:
                        st.error(f"Cannot connect to backend at {API_BASE}")

    with col_right:
        if "route_result" in st.session_state:
            data = st.session_state.route_result
            decision = data.get("route_decision")

            if decision:
                with st.container(border=True):
                    st.subheader("🧠 Route Decision")
                    metrics_cols = st.columns(4)
                    metrics_cols[0].metric("Query Type", decision["classified_type"])
                    metrics_cols[1].metric("Confidence", f"{decision['confidence']:.2f}")
                    metrics_cols[2].metric("Retrievers", ", ".join(decision["selected_retrievers"]))
                    metrics_cols[3].metric("Fusion", decision["fusion_method"])
                    st.markdown(f"**Why?** {decision['explanation']}")

            st.caption(f"Retrieved {len(data['results'])} results in {data['timing_ms']}ms")
            for i, doc in enumerate(data["results"], 1):
                with st.container(border=True):
                    cols = st.columns([1, 5, 1, 1])
                    cols[0].markdown(f"**#{i}**")
                    cols[1].markdown(doc["content"][:250] + ("..." if len(doc["content"]) > 250 else ""))
                    cols[2].markdown(f"`{doc['score']:.3f}`")
                    cols[3].markdown(doc.get("route", ""))

# ── Tab 3: Compare All ───────────────────────────────────────────────
with tab_compare:
    col_left, col_right = st.columns([1, 1])

    with col_left:
        cmp_query = st.text_area("Query", height=100, key="cmp_query",
                                  placeholder="Compare: What is the relationship between attention mechanisms and transformers?")
        cmp_top_k = st.slider("Top-K", min_value=3, max_value=20, value=5, key="cmp_top_k")

        if st.button("Compare All", type="primary", key="cmp_btn"):
            if cmp_query.strip():
                with st.spinner("Running all retrievers..."):
                    try:
                        resp = requests.post(
                            f"{API_BASE}/compare",
                            json={"query": cmp_query, "top_k": cmp_top_k},
                            timeout=180,
                        )
                        if resp.status_code == 200:
                            st.session_state.compare_result = resp.json()
                        else:
                            st.error(f"API Error: {resp.status_code} - {resp.text}")
                    except requests.exceptions.ConnectionError:
                        st.error(f"Cannot connect to backend at {API_BASE}")

    with col_right:
        if "compare_result" in st.session_state:
            data = st.session_state.compare_result
            strategies = data["strategies"]

            cols = st.columns(len(strategies))
            for i, (name, docs) in enumerate(strategies.items()):
                with cols[i]:
                    st.metric(name.title(), len(docs))

            tabs = st.tabs([s.title() for s in strategies.keys()])
            for tab_idx, (name, docs) in enumerate(strategies.items()):
                with tabs[tab_idx]:
                    for j, doc in enumerate(docs, 1):
                        with st.container(border=True):
                            st.markdown(f"**#{j}** — Score: `{doc['score']:.3f}`")
                            st.markdown(doc["content"][:200] + ("..." if len(doc["content"]) > 200 else ""))
