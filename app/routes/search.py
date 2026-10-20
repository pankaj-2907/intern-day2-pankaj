from fastapi import APIRouter, HTTPException, status
from app.schemas.search_schemas import SearchRequest, SearchResponse
from app.services.search_service import search_service

router = APIRouter(prefix="/search", tags=["Semantic Search"])

@router.post("", response_model=SearchResponse, status_code=status.HTTP_200_OK)
def perform_semantic_search(request: SearchRequest):
    """
    Executes semantic document search using Google text-embedding-004 vector embeddings
    and cosine similarity matching.
    """
    try:
        results = search_service.search(query=request.query, top_k=request.top_k)
        return SearchResponse(query=request.query, results=results)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Search failed: {str(e)}")