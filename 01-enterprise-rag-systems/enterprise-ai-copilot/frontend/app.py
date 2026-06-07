import streamlit as st
import requests
from datetime import datetime

API_BASE = "http://localhost:8000/api"

st.set_page_config(
    page_title="Enterprise AI Copilot",
    page_icon="🤖",
    layout="wide"
)

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []


def query_backend(prompt: str) -> dict | None:
    try:
        resp = requests.post(
            f"{API_BASE}/chat",
            json={
                "query": prompt,
                "conversation_id": st.session_state.conversation_id
            },
            timeout=60
        )
        if resp.status_code == 200:
            data = resp.json()
            st.session_state.conversation_id = data["conversation_id"]
            return data
        st.error(f"API Error: {resp.status_code} - {resp.text}")
        return None
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to backend. Ensure the API server is running on port 8000.")
        return None
    except Exception as e:
        st.error(f"Request failed: {e}")
        return None


def upload_document(file) -> dict | None:
    try:
        resp = requests.post(
            f"{API_BASE}/documents",
            files={"file": (file.name, file, file.type)},
            timeout=120
        )
        if resp.status_code == 200:
            return resp.json()
        st.error(f"Upload Error: {resp.status_code} - {resp.text}")
        return None
    except Exception as e:
        st.error(f"Upload failed: {e}")
        return None


st.title("Enterprise AI Copilot")
st.caption("RAG-powered assistant using LangChain + Pinecone + Groq")

tab_chat, tab_upload = st.tabs(["Chat", "Upload Documents"])

with tab_chat:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "sources" in msg and msg["sources"]:
                with st.expander("Sources", expanded=False):
                    for i, src in enumerate(msg["sources"]):
                        st.text_area(
                            f"Source {i+1}",
                            value=src["content"][:500],
                            height=100,
                            key=f"src_{msg['id']}_{i}"
                        )

    if prompt := st.chat_input("Ask a question about your documents..."):
        st.session_state.messages.append({"role": "user", "content": prompt, "id": str(datetime.now().timestamp())})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                result = query_backend(prompt)
            if result:
                st.markdown(result["answer"])
                if result["sources"]:
                    with st.expander("Sources", expanded=False):
                        for i, src in enumerate(result["sources"]):
                            st.text_area(
                                f"Source {i+1}",
                                value=src["content"][:500],
                                height=100,
                                key=f"src_{datetime.now().timestamp()}_{i}"
                            )
                st.caption(f"Processed in {result['processing_time_ms']:.0f}ms")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result["answer"],
                    "sources": result["sources"],
                    "id": str(datetime.now().timestamp())
                })

    if st.session_state.messages and st.button("Clear conversation"):
        st.session_state.messages = []
        st.session_state.conversation_id = None
        st.rerun()

with tab_upload:
    st.subheader("Upload a document")
    st.caption("Supported: PDF, TXT, MD, HTML, DOCX")

    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["pdf", "txt", "md", "html", "htm", "docx"]
    )

    if uploaded_file and st.button("Index Document"):
        with st.spinner("Processing and indexing..."):
            result = upload_document(uploaded_file)
        if result:
            st.success(
                f"Indexed **{result['filename']}** "
                f"— {result['chunks_count']} chunks created."
            )
