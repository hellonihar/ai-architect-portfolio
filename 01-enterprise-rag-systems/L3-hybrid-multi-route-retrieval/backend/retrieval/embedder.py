import logging

from sentence_transformers import SentenceTransformer

from core.config import settings

logger = logging.getLogger(__name__)


class Embedder:
    def __init__(self):
        logger.info("Loading embedding model: %s", settings.embedding_model)
        self.model = SentenceTransformer(settings.embedding_model)
        self.dimension = self.model.get_embedding_dimension()
        logger.info("Embedding dimension: %d", self.dimension)

    def encode(self, texts: list[str]) -> list[list[float]]:
        return self.model.encode(texts, show_progress_bar=False).tolist()

    def encode_single(self, text: str) -> list[float]:
        return self.model.encode([text], show_progress_bar=False).tolist()[0]
