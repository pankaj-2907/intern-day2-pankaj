# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import re
from ai_service import generate_ai_summary

app = FastAPI(title="Day 2 Assignment - FastAPI & Gemini AI")

# --- Pydantic Models for Request Validation ---
class TextAnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to analyze")

class TextSummarizeRequest(BaseModel):
    text: str = Field(..., min_length=20, description="Paragraph or text to summarize")


# --- Endpoint 1: Health Check ---
@app.get("/health")
def health_check():
    return {"status": "ok"}


# --- Endpoint 2: Text Analysis ---
@app.post("/text/analyze")
def analyze_text(payload: TextAnalyzeRequest):
    text = payload.text
    
    # Word count (using regex to count pure words)
    words = re.findall(r'\b\w+\b', text)
    word_count = len(words)
    
    # Character count (includes spaces and punctuation)
    character_count = len(text)
    
    # Uppercase text conversion
    uppercase_text = text.upper()
    
    return {
        "word_count": word_count,
        "character_count": character_count,
        "uppercase_text": uppercase_text
    }


# --- Endpoint 3: AI Summarization ---
@app.post("/text/summarize")
def summarize_text_endpoint(payload: TextSummarizeRequest):
    try:
        # Calling AI service to summarize
        summary = generate_ai_summary(payload.text)
        return {"summary": summary}
    
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")