class ResponseFormatter:
    def format(self, answer: str, sources: list[dict], conversation_id: str, processing_time_ms: float) -> dict:
        return {
            "answer": answer,
            "sources": sources,
            "conversation_id": conversation_id,
            "processing_time_ms": round(processing_time_ms, 2)
        }
