from celery import shared_task
from django.utils import timezone
from .models import Document, Chunk
from apps.indexing.services.retriever import get_embedding_function


@shared_task
def process_document(document_id):
    try:
        doc = Document.objects.get(id=document_id)
        doc.status = "processing"
        doc.save()

        # Extract text from file
        text = extract_text(doc.file.path)
        chunks = chunk_text(text)

        # Generate embeddings and store chunks
        embedding_fn = get_embedding_function()
        for i, chunk_content in enumerate(chunks):
            embedding = embedding_fn.embed_query(chunk_content)
            chunk = Chunk.objects.create(
                document=doc,
                content=chunk_content,
                chunk_index=i,
                metadata={"length": len(chunk_content)},
            )
            # Store embedding in Pinecone via retriever service
            from apps.indexing.services.pinecone_client import upsert_embedding
            upsert_embedding(str(chunk.id), embedding, {"document_id": str(doc.id), "chunk_index": i})

        doc.status = "indexed"
        doc.processed_at = timezone.now()
        doc.page_count = len(chunks)
        doc.save()

    except Exception as e:
        doc.status = "failed"
        doc.error_message = str(e)
        doc.save()


def extract_text(file_path):
    import pypdf
    text = []
    with open(file_path, "rb") as f:
        reader = pypdf.PdfReader(f)
        for page in reader.pages:
            text.append(page.extract_text())
    return "\n".join(text)


def chunk_text(text, chunk_size=1000, overlap=200):
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    return splitter.split_text(text)
