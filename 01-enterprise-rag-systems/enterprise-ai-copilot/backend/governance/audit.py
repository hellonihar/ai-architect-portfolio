import logging
import datetime

logger = logging.getLogger(__name__)


class AuditLogger:
    def log_query(self, query: str, conversation_id: str, status: str, processing_time_ms: float):
        logger.info(
            f"AUDIT|{datetime.datetime.utcnow().isoformat()}|"
            f"{conversation_id}|{status}|{processing_time_ms:.2f}ms|"
            f"query={query[:200]}"
        )

    def log_ingestion(self, filename: str, chunks_count: int, document_id: str, status: str):
        logger.info(
            f"AUDIT|{datetime.datetime.utcnow().isoformat()}|"
            f"INGEST|{document_id}|{filename}|{chunks_count} chunks|{status}"
        )
