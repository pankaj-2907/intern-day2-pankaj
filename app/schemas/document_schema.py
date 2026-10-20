from pydantic import BaseModel, Field

class DocumentCreate(BaseModel):
    id: str = Field(..., min_length=1, description="Unique identifier for the document")
    title: str = Field(..., min_length=1, description="Title of the document")
    content: str = Field(..., min_length=1, description="Main text content of the document")