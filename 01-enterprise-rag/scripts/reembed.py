#!/usr/bin/env python
"""
Re-embed all document chunks with the latest embedding model.
Usage: python scripts/reembed.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "enterprise_rag.settings")

import django
django.setup()

from apps.ingestion.models import Chunk
from apps.indexing.services.retriever import get_embedding_function
from apps.indexing.services.pinecone_client import upsert_embedding


def reembed_all():
    embedding_fn = get_embedding_function()
    chunks = Chunk.objects.all()
    print(f"Re-embedding {chunks.count()} chunks...")
    for chunk in chunks:
        embedding = embedding_fn.embed_query(chunk.content)
        upsert_embedding(str(chunk.id), embedding, {"document_id": str(chunk.document_id), "chunk_index": chunk.chunk_index})
        chunk.embedding_id = str(chunk.id)
        chunk.save()
    print("Done.")


if __name__ == "__main__":
    reembed_all()
