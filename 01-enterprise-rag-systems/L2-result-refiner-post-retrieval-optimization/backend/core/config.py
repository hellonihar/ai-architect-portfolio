from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    groq_api_key: str = ""
    groq_model: str = "qwen/qwen3-32b"
    groq_temperature: float = 0.1
    max_input_length: int = 4096

    embedding_model: str = "BAAI/bge-small-en-v1.5"
    cross_encoder_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"

    top_k: int = 10
    rerank_top_k: int = 5

    sliding_window_threshold: float = 0.3
    sliding_window_token_budget: int = 4096

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parent.parent.parent / ".env"),
        env_file_encoding="utf-8",
    )


settings = Settings()
