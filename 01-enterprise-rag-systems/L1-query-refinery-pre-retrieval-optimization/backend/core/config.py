from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    groq_api_key: str = ""
    groq_model: str = "qwen/qwen3-32b"
    groq_temperature: float = 0.3
    max_input_length: int = 4096

    embedding_model: str = "BAAI/bge-small-en-v1.5"

    refinery_default_strategy: str = "auto"
    multi_query_variants: int = 3
    hyde_temperature: float = 0.3
    rewriter_use_history: bool = True

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parent.parent.parent / ".env"),
        env_file_encoding="utf-8",
    )


settings = Settings()
