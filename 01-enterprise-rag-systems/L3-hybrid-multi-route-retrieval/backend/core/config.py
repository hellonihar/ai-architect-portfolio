from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    groq_api_key: str = ""
    groq_model: str = "qwen/qwen3-32b"
    groq_temperature: float = 0.0

    embedding_model: str = "BAAI/bge-small-en-v1.5"

    top_k: int = 10
    hybrid_alpha: float = 0.5

    fusion_method: str = "rrf"
    rrf_constant: int = 60

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parent.parent.parent / ".env"),
        env_file_encoding="utf-8",
    )


settings = Settings()
