from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator
from app.services.retrieval_service import RetrievalService

# Global instance
_default_retrieval_service = RetrievalService()

class KBQueryInput(BaseModel):
    query: str = Field(..., description="Search query string")
    top_k: int = Field(default=3, description="Number of results to retrieve (1 to 10)")

    @field_validator("query")
    @classmethod
    def validate_query(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("Query string cannot be empty.")
        return stripped

    @field_validator("top_k")
    @classmethod
    def validate_top_k(cls, v: int) -> int:
        if v < 1 or v > 10:
            raise ValueError("top_k must be an integer between 1 and 10.")
        return v


def search_knowledge_base(query: str, top_k: int = 3, retrieval_service: Optional[Any] = None) -> Dict[str, Any]:
    """
    Searches indexed documents using the underlying retrieval service.
    """
    try:
        validated = KBQueryInput(query=query, top_k=top_k)
    except Exception as e:
        return {"error": f"Invalid search input: {str(e)}", "results": [], "success": False}

    # Fallback to default module instance if none provided at runtime
    active_service = retrieval_service if retrieval_service is not None else _default_retrieval_service

    if active_service is None or not getattr(active_service, "chunks", None):
        return {
            "results": [],
            "message": "Retrieval service is not initialized or indexed documents are empty.",
            "success": True
        }

    try:
        results = active_service.search(query=validated.query, top_k=validated.top_k)
        formatted_results = []
        for item in results:
            formatted_results.append({
                "document_id": getattr(item, "document_id", getattr(item, "id", "doc_unknown")),
                "title": getattr(item, "title", "Untitled Document"),
                "content": getattr(item, "content", getattr(item, "text", "")),
                "score": float(getattr(item, "score", 0.0))
            })
        return {
            "results": formatted_results,
            "count": len(formatted_results),
            "success": True
        }
    except Exception as e:
        return {
            "error": f"Retrieval failed: {str(e)}",
            "results": [],
            "success": False
        }