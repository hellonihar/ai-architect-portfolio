from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    groq_api_key: str = ""
    groq_model: str = "qwen/qwen3-32b"
    groq_temperature: float = 0.0

    embedding_model: str = "BAAI/bge-small-en-v1.5"

    top_k: int = 10
    rrf_constant: int = 60

    relevance_threshold: float = 0.5
    quality_threshold: float = 0.6
    complexity_threshold: float = 0.7
    max_hops: int = 3

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parent.parent.parent / ".env"),
        env_file_encoding="utf-8",
    )


settings = Settings()
