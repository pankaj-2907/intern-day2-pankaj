from pydantic import BaseModel, Field
from typing import Optional

# --- Summarize Schemas ---
class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=10, description="Text to be summarized")

class SummarizeResponse(BaseModel):
    summary: str


# --- Classify Schemas ---
class ClassifyRequest(BaseModel):
    text: str = Field(..., min_length=5, description="Text to be classified")

class ClassifyResponse(BaseModel):
    category: str
    confidence: Optional[float] = None
    reasoning: str


# --- Sentiment Schemas ---
class SentimentRequest(BaseModel):
    text: str = Field(..., min_length=3, description="Text for sentiment analysis")

class SentimentResponse(BaseModel):
    sentiment: str  # e.g., Positive, Neutral, Negative
    score: Optional[float] = None
    explanation: str