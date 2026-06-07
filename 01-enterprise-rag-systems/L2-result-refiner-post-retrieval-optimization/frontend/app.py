import streamlit as st
import requests
import os

API_BASE = os.getenv("API_BASE", "http://localhost:8001")

st.set_page_config(page_title="L2 Result Refiner", page_icon="🎯", layout="wide")
st.title("L2 Result Refiner — Post-Retrieval Optimization")
st.caption("Compare reranking, context compression, small-to-big expansion, and sliding window side by side.")

tab_refine, tab_compare = st.tabs(["Refine", "Compare All Strategies"])

with tab_refine:
    col_left, col_right = st.columns([1, 1])

    with col_left:
        query = st.text_area("Query", height=100, placeholder="What is RAG and how does it work?")
        strategy = st.selectbox(
            "Strategy",
            ["reranker", "compressor", "small_to_big", "sliding_window"],
            help="reranker: cross-encoder re-scoring | compressor: LLM-based filtering | small_to_big: parent expansion | sliding_window: dynamic context sizing",
        )
        top_k = st.slider("Top-K chunks to retrieve", min_value=3, max_value=20, value=10)

        if st.button("Refine", type="primary"):
            if query.strip():
                with st.spinner(f"Running {strategy}..."):
                    try:
                        resp = requests.post(
                            f"{API_BASE}/refine",
                            json={"query": query, "strategy": strategy, "top_k": top_k},
                            timeout=120,
                        )
                        if resp.status_code == 200:
                            st.session_state.refine_result = resp.json()
                        else:
                            st.error(f"API Error: {resp.status_code} - {resp.text}")
                    except requests.exceptions.ConnectionError:
                        st.error(f"Cannot connect to backend at {API_BASE}")

    with col_right:
        if "refine_result" in st.session_state:
            data = st.session_state.refine_result

            st.subheader(f"Strategy: {data['strategy']}")
            st.markdown(f"**Explanation:** {data['explanation']}")

            raw_tab, refined_tab = st.tabs(["Raw Results", f"Refined ({data['strategy']})"])

            with raw_tab:
                st.markdown(f"**{len(data['raw_results'])} chunks retrieved**")
                for i, doc in enumerate(data["raw_results"], 1):
                    with st.container(border=True):
                        cols = st.columns([1, 5, 1])
                        cols[0].markdown(f"**#{i}**")
                        cols[1].markdown(doc["content"][:200] + ("..." if len(doc["content"]) > 200 else ""))
                        cols[2].markdown(f"`{doc['score']:.3f}`")

            with refined_tab:
                docs = data["refined_results"]
                st.markdown(f"**{len(docs)} chunks after refinement**")
                for i, doc in enumerate(docs, 1):
                    with st.container(border=True):
                        cols = st.columns([1, 5, 1])
                        cols[0].markdown(f"**#{i}**")
                        score_label = f"`{doc['score']:.3f}`"
                        if "cross_encoder_score" in doc.get("metadata", {}):
                            score_label = f"CE: `{doc['metadata']['cross_encoder_score']:.3f}`"
                        cols[2].markdown(score_label)
                        cols[1].markdown(doc["content"][:300] + ("..." if len(doc["content"]) > 300 else ""))

            if data["metadata"]:
                with st.expander("Metadata", expanded=False):
                    st.json(data["metadata"])

with tab_compare:
    col_left, col_right = st.columns([1, 1])

    with col_left:
        cmp_query = st.text_area("Query", height=100, key="cmp_query", placeholder="What are vector databases?")
        cmp_top_k = st.slider("Top-K", min_value=3, max_value=20, value=10, key="cmp_top_k")

        if st.button("Compare All", type="primary", key="cmp_btn"):
            if cmp_query.strip():
                with st.spinner("Running all 4 strategies..."):
                    try:
                        resp = requests.post(
                            f"{API_BASE}/evaluate",
                            json={"query": cmp_query, "top_k": cmp_top_k},
                            timeout=180,
                        )
                        if resp.status_code == 200:
                            st.session_state.eval_result = resp.json()
                        else:
                            st.error(f"API Error: {resp.status_code} - {resp.text}")
                    except requests.exceptions.ConnectionError:
                        st.error(f"Cannot connect to backend at {API_BASE}")

    with col_right:
        if "eval_result" in st.session_state:
            data = st.session_state.eval_result

            st.subheader("All Strategies Comparison")

            raw_count = len(data["raw_results"])
            st.metric("Raw retrieved chunks", raw_count)

            comp_cols = st.columns(4)
            for i, (name, result) in enumerate(data["strategies"].items()):
                count = len(result["refined_results"])
                display_name = name.replace("_", " ").title()
                with comp_cols[i]:
                    st.metric(display_name, count, delta=count - raw_count)

            tabs = st.tabs(["Raw"] + [s.replace("_", " ").title() for s in data["strategies"].keys()])

            with tabs[0]:
                for i, doc in enumerate(data["raw_results"], 1):
                    with st.container(border=True):
                        st.markdown(f"**#{i}** — Score: `{doc['score']:.3f}`")
                        st.markdown(doc["content"][:200] + ("..." if len(doc["content"]) > 200 else ""))

            for tab_idx, (name, result) in enumerate(data["strategies"].items(), 1):
                with tabs[tab_idx]:
                    st.markdown(f"**{result['explanation']}**")
                    for i, doc in enumerate(result["refined_results"], 1):
                        with st.container(border=True):
                            st.markdown(f"**#{i}** — Score: `{doc['score']:.3f}`")
                            st.markdown(doc["content"][:300] + ("..." if len(doc["content"]) > 300 else ""))
