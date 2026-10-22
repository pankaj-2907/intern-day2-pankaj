from fastapi import APIRouter, HTTPException, status
from app.schemas.rag_schemas import AskRequest, AskResponse, HealthResponse, SourcesListResponse, SourceItem
from app.services.rag_service import RAGService
from app.services.retrieval_service import RetrievalService
import json
import os

router = APIRouter(prefix="/rag", tags=["RAG Question Answering"])

# Initialize services singleton
retrieval_service = RetrievalService()
rag_service = RAGService(retrieval_service=retrieval_service)

@router.post("/ask", response_model=AskResponse, status_code=status.HTTP_200_OK)
def ask_question(payload: AskRequest):
    """
    Accepts a question and top_k, retrieves relevant chunks, and generates a grounded RAG answer.
    """
    try:
        result = rag_service.generate_answer(question=payload.question, top_k=payload.top_k)
        return result
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve))
    except RuntimeError as re:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(re))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/health", response_model=HealthResponse, status_code=status.HTTP_200_OK)
def rag_health():
    """
    Reflects actual application readiness based on index and service availability.
    """
    try:
        # Check if index has loaded chunks properly
        if not retrieval_service.chunks:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Retrieval index is empty")
        return {"status": "ok"}
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))

@router.get("/sources", response_model=SourcesListResponse, status_code=status.HTTP_200_OK)
def list_sources():
    """
    Returns available source documents with IDs and titles without exposing raw embeddings.
    """
    path = "data/documents.json"
    if not os.path.exists(path):
        return {"sources": []}
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            docs = json.load(f)
        
        source_items = [SourceItem(id=d["id"], title=d["title"]) for d in docs]
        return {"sources": source_items}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to load sources")