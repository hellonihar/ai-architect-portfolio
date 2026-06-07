from langchain_text_splitters import RecursiveCharacterTextSplitter

from core.config import settings


class TextChunker:
    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]
        )

    def chunk(self, documents: list[dict]) -> list[dict]:
        texts = [doc["content"] for doc in documents]
        metadatas = [doc["metadata"] for doc in documents]
        chunks = self.splitter.create_documents(texts, metadatas=metadatas)
        return [
            {
                "content": chunk.page_content,
                "metadata": chunk.metadata
            }
            for chunk in chunks
        ]
