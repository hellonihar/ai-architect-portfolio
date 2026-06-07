class ContextBuilder:
    def build(self, documents: list[dict], max_length: int = 4096) -> str:
        chunks = []
        total = 0
        for doc in documents:
            content = doc.get("content", "")
            source = doc.get("metadata", {}).get("source", "unknown")
            chunk = f"[Source: {source}]\n{content}"
            if total + len(chunk) > max_length:
                break
            chunks.append(chunk)
            total += len(chunk)
        return "\n\n".join(chunks)

    def format_sources(self, documents: list[dict]) -> list[dict]:
        return [
            {
                "content": doc.get("content", ""),
                "metadata": doc.get("metadata", {})
            }
            for doc in documents
        ]
