from core.config import settings


class Reranker:
    def rerank(self, query: str, documents: list[dict], top_k: int = 3) -> list[dict]:
        if not settings.enable_reranking:
            return documents[:top_k]
        return sorted(documents, key=lambda x: x.get("score", 0), reverse=True)[:top_k]
