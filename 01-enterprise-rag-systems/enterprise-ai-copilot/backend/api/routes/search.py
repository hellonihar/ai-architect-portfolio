from fastapi import APIRouter

from api.schemas import SearchRequest, SearchResult

router = APIRouter()
retriever = None


def get_retriever():
    global retriever
    if retriever is None:
        from rag.retrieval.vector import PineconeRetriever
        retriever = PineconeRetriever()
    return retriever


@router.post("/search", response_model=list[SearchResult])
async def search(request: SearchRequest):
    results = get_retriever().retrieve(request.query, top_k=request.top_k)
    return [SearchResult(**r) for r in results]
