from pydantic import BaseModel, Field
from typing import List

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Natural language search query")
    top_k: int = Field(default=3, ge=1, le=20, description="Number of top matching results to return")

class SearchResultItem(BaseModel):
    id: str
    title: str
    content: str
    score: float

class SearchResponse(BaseModel):
    query: str
    results: List[SearchResultItem]