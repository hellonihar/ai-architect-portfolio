import streamlit as st
import requests

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="L1 Query Refinery", page_icon="🔍", layout="wide")
st.title("L1 Query Refinery — Pre-Retrieval Optimization")
st.caption("Compare query rewriting, HyDE, multi-query expansion, and query decomposition side by side.")

tab_refine, tab_evaluate = st.tabs(["Refine", "Evaluate"])

with tab_refine:
    col_left, col_right = st.columns([1, 1])

    with col_left:
        query = st.text_area("Raw query", height=100)
        strategy = st.selectbox(
            "Strategy",
            ["auto", "query_rewriter", "hyde", "multi_query", "query_decomposer"],
        )
        history_text = st.text_area("Conversation history (one per line)", height=80, placeholder="What is RAG?\nit helps with...")

        if st.button("Refine", type="primary"):
            if query.strip():
                history = [h.strip() for h in history_text.split("\n") if h.strip()] if history_text else None
                with st.spinner("Refining..."):
                    try:
                        resp = requests.post(
                            f"{API_BASE}/refine",
                            json={"query": query, "strategy": strategy, "conversation_history": history},
                            timeout=30,
                        )
                        if resp.status_code == 200:
                            data = resp.json()
                            st.session_state.refine_result = data
                        else:
                            st.error(f"API Error: {resp.status_code} - {resp.text}")
                    except requests.exceptions.ConnectionError:
                        st.error("Cannot connect to backend on port 8000")

    with col_right:
        if "refine_result" in st.session_state:
            data = st.session_state.refine_result
            st.subheader(f"Strategy: {data['strategy']}")
            st.markdown(f"**Explanation:** {data['explanation']}")
            st.markdown("**Refined queries:**")
            for i, q in enumerate(data["refined_queries"], 1):
                st.code(q, language="text")
            if data["metadata"]:
                with st.expander("Metadata", expanded=False):
                    st.json(data["metadata"])

with tab_evaluate:
    col_left, col_right = st.columns([1, 1])

    with col_left:
        eval_query = st.text_area("Query to evaluate", height=100, key="eval_query")
        eval_strategy = st.selectbox(
            "Strategy",
            ["auto", "query_rewriter", "hyde", "multi_query", "query_decomposer"],
            key="eval_strategy",
        )

        if st.button("Evaluate", type="primary", key="eval_btn"):
            if eval_query.strip():
                with st.spinner("Evaluating..."):
                    try:
                        resp = requests.post(
                            f"{API_BASE}/evaluate",
                            json={"query": eval_query, "strategy": eval_strategy},
                            timeout=30,
                        )
                        if resp.status_code == 200:
                            data = resp.json()
                            st.session_state.eval_result = data
                        else:
                            st.error(f"API Error: {resp.status_code} - {resp.text}")
                    except requests.exceptions.ConnectionError:
                        st.error("Cannot connect to backend on port 8000")

    with col_right:
        if "eval_result" in st.session_state:
            data = st.session_state.eval_result
            st.subheader(f"Strategy: {data['strategy']}")

            st.markdown("**Raw query:**")
            st.code(data["raw_queries"][0], language="text")
            st.markdown("**Refined query:**")
            st.code(data["refined_queries"][0], language="text")

            st.markdown("**Scores (1-10):**")
            for score in data["scores"]:
                delta = score["refined_score"] - score["raw_score"]
                sign = "+" if delta > 0 else ""
                st.metric(
                    label=score["criterion"],
                    value=f"{score['refined_score']} / 10",
                    delta=f"{sign}{delta} vs raw ({score['raw_score']})",
                    help=score["explanation"],
                )
