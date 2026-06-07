from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    groq_api_key: str = ""
    groq_model: str = "qwen/qwen3-32b"
    pinecone_api_key: str = (
        "pcsk_29LhLG_2w5bP3gUm5Hk4UVEaagbf61kY58xd8XQUcnjLCiz3tyrCqWNNupmtkSc9Ppq1wz"
    )
    pinecone_environment: str = "us-east-1"
    pinecone_index: str = "enterprise-copilot"
    embedding_model: str = "BAAI/bge-small-en-v1.5"
    chunk_size: int = 512
    chunk_overlap: int = 64
    top_k: int = 5
    rerank_top_k: int = 3
    enable_reranking: bool = False
    max_input_length: int = 4096
    enable_guardrails: bool = True
    enable_audit: bool = True

    class Config:
        env_file = str(Path(__file__).resolve().parent.parent.parent / ".env")
        env_file_encoding = "utf-8"


settings = Settings()
