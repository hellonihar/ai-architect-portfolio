from langchain_huggingface import HuggingFaceEmbeddings

from core.config import settings


class Embedder:
    def __init__(self):
        self.client = HuggingFaceEmbeddings(model_name=settings.embedding_model)

    def embed(self, text: str) -> list[float]:
        return self.client.embed_query(text)
