import tempfile
from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredMarkdownLoader,
    UnstructuredHTMLLoader,
    UnstructuredWordDocumentLoader,
)


class DocumentLoader:
    SUPPORTED_EXTENSIONS = {
        ".pdf": PyPDFLoader,
        ".txt": TextLoader,
        ".md": UnstructuredMarkdownLoader,
        ".html": UnstructuredHTMLLoader,
        ".htm": UnstructuredHTMLLoader,
        ".docx": UnstructuredWordDocumentLoader,
    }

    def load(self, file_content: bytes, filename: str) -> list[dict]:
        ext = Path(filename).suffix.lower()
        if ext not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported file type: {ext}")

        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            tmp.write(file_content)
            tmp_path = tmp.name

        try:
            loader_cls = self.SUPPORTED_EXTENSIONS[ext]
            loader = loader_cls(tmp_path)
            docs = loader.load()
            return [
                {
                    "content": doc.page_content,
                    "metadata": {**doc.metadata, "source": filename}
                }
                for doc in docs
            ]
        finally:
            Path(tmp_path).unlink(missing_ok=True)
