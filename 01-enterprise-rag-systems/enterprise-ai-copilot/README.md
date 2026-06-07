# Enterprise AI Copilot

RAG-powered enterprise assistant using LangChain, Pinecone, and Qwen.

## Architecture

```
User → Streamlit Frontend → FastAPI Backend → Pinecone (Vector DB)
                            → LangChain (RAG Pipeline)
                            → Qwen (LLM Inference)
```

## Prerequisites

- Python 3.11+
- A [Groq API key](https://console.groq.com) (for Qwen access)
- A [Pinecone API key](https://www.pinecone.io)

## Quick Start

1. Clone the repo and navigate to this directory:
   ```bash
   cd 01-enterprise-rag-systems/enterprise-ai-copilot
   ```

2. Copy and fill in environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. Start with Docker:
   ```bash
   docker compose up --build
   ```
   Backend: http://localhost:8000  
   Frontend: http://localhost:8501

## Without Docker

### Backend
```bash
cd backend
pip install -r requirements.txt
cp ../.env .
uvicorn api.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py --server.port=8501
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/chat` | Ask a question (RAG-powered) |
| POST | `/api/documents` | Upload and index a document |
| POST | `/api/search` | Standalone vector search |
| GET  | `/health` | Health check |

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI (Python) |
| RAG Framework | LangChain |
| Vector Store | Pinecone |
| LLM | Qwen (Qwen3-32b via Groq) |
| Embeddings | BGE (sentence-transformers) |
| Frontend | Streamlit |
| Containerization | Docker + docker-compose |
