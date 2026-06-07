import logging
import time

import numpy as np

from core.config import settings
from data.sample_corpus import CHILD_CHUNKS, PARENT_DOCUMENTS
from refiner.embedder import Embedder

logger = logging.getLogger(__name__)


class InMemoryRetriever:
    def __init__(self):
        self.embedder = Embedder()
        self.child_chunks = CHILD_CHUNKS
        self.parent_docs = {d["id"]: d for d in PARENT_DOCUMENTS}

        self.chunk_texts = [c["content"] for c in self.child_chunks]
        logger.info(f"Embedding {len(self.chunk_texts)} corpus chunks...")
        self.chunk_embeddings = np.array(self.embedder.embed_batch(self.chunk_texts))
        self.corpus_size = len(self.child_chunks)
        logger.info(f"Corpus indexed: {self.corpus_size} chunks across {len(self.parent_docs)} parents")

    def retrieve(self, query: str, top_k: int = 10) -> list[dict]:
        start = time.time()
        query_embedding = np.array(self.embedder.embed(query))

        scores = np.dot(self.chunk_embeddings, query_embedding)
        top_indices = np.argsort(scores)[::-1][:top_k]

        results = []
        for idx in top_indices:
            chunk = self.child_chunks[idx]
            results.append({
                "id": chunk["id"],
                "content": chunk["content"],
                "score": float(scores[idx]),
                "parent_id": chunk.get("parent_id"),
                "metadata": {
                    "parent_title": self.parent_docs.get(chunk.get("parent_id", ""), {}).get("title", ""),
                },
            })

        elapsed = (time.time() - start) * 1000
        logger.info(f"Retrieved {len(results)} results in {elapsed:.0f}ms")
        return results

    def get_parent_content(self, parent_id: str) -> str | None:
        doc = self.parent_docs.get(parent_id)
        return doc["content"] if doc else None

    def get_all_parents(self) -> list[dict]:
        return list(self.parent_docs.values())
