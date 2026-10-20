from fastapi import APIRouter, HTTPException, status
from app.schemas.document_schema import DocumentCreate
from app.services.search_service import search_service

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("", status_code=status.HTTP_201_CREATED)
def add_document(doc: DocumentCreate):
    """
    Add a new document to the in-memory index.
    - Validates input.
    - Rejects duplicate IDs (400 Bad Request).
    - Generates embedding and stores it.
    """
    try:
        search_service.add_document(doc.id, doc.title, doc.content)
        return {
            "message": "Document added successfully",
            "id": doc.id,
            "title": doc.title
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", status_code=status.HTTP_200_OK)
def list_documents():
    """
    Retrieve a list of all available documents (IDs and titles only, no raw embeddings).
    """
    return search_service.get_all_documents()