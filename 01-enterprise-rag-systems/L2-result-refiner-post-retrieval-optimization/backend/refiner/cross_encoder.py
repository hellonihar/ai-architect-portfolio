import logging

from sentence_transformers import CrossEncoder

from core.config import settings

logger = logging.getLogger(__name__)


class CrossEncoderClient:
    def __init__(self):
        logger.info(f"Loading cross-encoder: {settings.cross_encoder_model}")
        self.model = CrossEncoder(settings.cross_encoder_model)

    def score(self, pairs: list[tuple[str, str]]) -> list[float]:
        return self.model.predict(pairs).tolist()
