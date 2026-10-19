# ai 

from fastapi import APIRouter, HTTPException
from app.schemas.ai_schemas import (
    SummarizeRequest, SummarizeResponse,
    ClassifyRequest, ClassifyResponse,
    SentimentRequest, SentimentResponse
)
from app.services.llm_service import (
    generate_summary,
    generate_classification,
    generate_sentiment
)

router = APIRouter(prefix="/ai", tags=["AI Text Intelligence"])

@router.post("/summarize", response_model=SummarizeResponse)
def summarize_text(payload: SummarizeRequest):
    """API endpoint to generate text summary."""
    try:
        summary_text = generate_summary(payload.text)
        return SummarizeResponse(summary=summary_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/classify", response_model=ClassifyResponse)
def classify_text(payload: ClassifyRequest):
    """API endpoint to classify text into categories."""
    try:
        result = generate_classification(payload.text)
        return ClassifyResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sentiment", response_model=SentimentResponse)
def analyze_sentiment(payload: SentimentRequest):
    """API endpoint to analyze the sentiment of the text."""
    try:
        result = generate_sentiment(payload.text)
        return SentimentResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))