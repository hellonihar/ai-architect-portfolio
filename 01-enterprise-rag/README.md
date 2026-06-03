# Enterprise Retrieval-Augmented Generation (RAG) System

## Problem Statement
Enterprises struggle with knowledge retrieval across siloed systems. Traditional search lacks semantic depth, while LLMs hallucinate without grounding.

## Solution
A Django-based RAG pipeline implementing document ingestion, hybrid retrieval (semantic + BM25), conversational QA via Groq LLMs, with built-in observability and governance.

## Architecture

![Architecture Diagram](diagrams/image.png)

The system is composed of six Django apps:

| App | Responsibility |
|-----|---------------|
| **ingestion** | REST API for document upload (PDF, Word); Celery background task for text extraction, chunking, embedding, and Pinecone upsert |
| **indexing** | Hybrid retrieval — semantic search on Pinecone fused with Elasticsearch BM25 via Reciprocal Rank Fusion (RRF) |
| **chat** | Conversational QA with context retrieval and citation-enforced LLM responses |
| **governance** | Audit logging (action/resource/user tracking) and bias keyword detection |
| **observability** | Prometheus middleware collecting request count, latency, token usage, and drift metrics |
| **ui** | Tailwind CSS frontend (chat, search, dashboard, admin pages) |

## Tech Stack

| Category | Technology |
|----------|------------|
| Backend | Django 5, Django REST Framework, Celery + Redis, PostgreSQL |
| Embeddings | OpenAI `text-embedding-3-small` (1536d) |
| Vector Store | Pinecone (serverless, cosine metric) |
| Keyword Search | Elasticsearch (BM25) |
| Fusion | Custom Reciprocal Rank Fusion (RRF) |
| LLM | Groq — Mixtral 8x7b (configurable via `GROQ_MODEL` env var) |
| Orchestration | LangChain (text splitting via `RecursiveCharacterTextSplitter`, embeddings wrapper) |
| Document Processing | pypdf (PDF), python-docx (Word) |
| Observability | Prometheus client, OpenTelemetry SDK |
| Governance | Audit logging (Django models + DRF viewset), bias keyword audit script |
| Frontend | Tailwind CSS (via CDN) — chat, search, dashboard, admin |

## Applied Best Practices
- **Hybrid retrieval** combines keyword precision (BM25) with semantic recall (dense embeddings)
- **Citation enforcement** via system prompt ensures LLM responses are grounded in retrieved sources
- **Modular Django app design** enables independent development and testing of each pipeline stage

## Alternatives Considered

| Option | Status | Trade-off |
|--------|--------|-----------|
| **Weaviate** | Not used | Richer vector features; heavier operational overhead |
| **ChromaDB** | Dependency listed, unused | Lightweight, good for prototyping; lacks production scalability |
| **FAISS** | Not used | Fast local ANN search; no managed cloud option |
| **Milvus** | Not used | Scalable open-source; higher ops complexity |

## Limitations
- Latency increases with large-scale queries
- Requires strong data governance to prevent leakage
- Cost optimization critical for enterprise-scale deployments

## Getting Started

### Prerequisites
- Python 3.11+
- PostgreSQL
- Redis
- Elasticsearch 8.x
- Pinecone account
- Groq API key
- OpenAI API key

### Environment Variables
```
OPENAI_API_KEY=
PINECONE_API_KEY=
PINECONE_INDEX_NAME=
GROQ_API_KEY=
GROQ_MODEL=mixtral-8x7b-32768
ELASTICSEARCH_URL=http://localhost:9200
DATABASE_URL=postgresql://user:pass@localhost:5432/enterprise_rag
```

### Quick Start
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
