import logging
import numpy as np

logger = logging.getLogger(__name__)


class Embedder:
    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or "BAAI/bge-small-en-v1.5"
        self._model = None

    def _load_model(self):
        try:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(self.model_name)
            logger.info("Loaded embedding model: %s (dim=%d)", self.model_name, self._model.get_sentence_embedding_dimension())
        except Exception as e:
            logger.warning("Failed to load embedding model '%s': %s. Using fallback random embeddings.", self.model_name, e)
            self._model = None

    def embed(self, texts: list[str]) -> np.ndarray:
        if self._model is None:
            self._load_model()
        if self._model is not None:
            return self._model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
        return np.random.randn(len(texts), 384).astype(np.float32)

    def embed_single(self, text: str) -> np.ndarray:
        return self.embed([text])[0]

    @property
    def dimension(self) -> int:
        if self._model is not None:
            return self._model.get_sentence_embedding_dimension()
        return 384
