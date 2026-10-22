from pydantic import BaseModel, Field
from typing import List, Optional

class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, description="The natural language question to ask")
    top_k: int = Field(default=3, ge=1, le=10, description="Number of top chunks to retrieve")

class SourceReference(BaseModel):
    document_id: str
    title: str
    chunk_id: str

class AskResponse(BaseModel):
    question: str
    answer: str
    sources: List[SourceReference]
    retrieved_chunks: int

class HealthResponse(BaseModel):
    status: str

class SourceItem(BaseModel):
    id: str
    title: str

class SourcesListResponse(BaseModel):
    sources: List[SourceItem]