import uuid
import logging

from fastapi import APIRouter, UploadFile, File, HTTPException

from api.schemas import DocumentUploadResponse
from governance.audit import AuditLogger
from core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()
audit = AuditLogger()
doc_loader = None
text_chunker = None
indexer = None


def get_loader():
    global doc_loader
    if doc_loader is None:
        from ingestion.loader import DocumentLoader
        doc_loader = DocumentLoader()
    return doc_loader


def get_chunker():
    global text_chunker
    if text_chunker is None:
        from ingestion.chunker import TextChunker
        text_chunker = TextChunker()
    return text_chunker


def get_indexer():
    global indexer
    if indexer is None:
        from ingestion.indexer import PineconeIndexer
        indexer = PineconeIndexer()
    return indexer


@router.post("/documents", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided.")

    content = await file.read()
    doc_id = str(uuid.uuid4())

    try:
        docs = get_loader().load(content, file.filename)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    chunks = get_chunker().chunk(docs)
    num_chunks = get_indexer().index(chunks)

    if settings.enable_audit:
        audit.log_ingestion(
            filename=file.filename,
            chunks_count=num_chunks,
            document_id=doc_id,
            status="success"
        )

    return DocumentUploadResponse(
        document_id=doc_id,
        filename=file.filename,
        chunks_count=num_chunks,
        status="indexed"
    )
