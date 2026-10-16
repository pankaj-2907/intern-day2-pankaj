# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import re
from ai_service import generate_ai_summary, translate_text
from collections import Counter

app = FastAPI(title="Day 2 Assignment - FastAPI & Gemini AI")

# --- Pydantic Models for Request Validation ---
class TextAnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to analyze")

class TextSummarizeRequest(BaseModel):
    text: str = Field(..., min_length=20, description="Paragraph or text to summarize")

class TextTranslateRequest(BaseModel):
    text: str = Field(..., min_length=15, description="Paragraph or text to translate")

class WordFrequencyRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text for word frequency analysis")


# --- Endpoint 1: Health Check ---
@app.get("/health")
def health_check():
    return {"status": "healthy", 
            "service": "running",
            "checks_passed": True}
    

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

# --- Endpoint 4: AI Translation ---
@app.post("/text/translate")
def translate_text_endpoint(payload: TextTranslateRequest):
    try:
        # Calling AI service to translate
        translation = translate_text(payload.text)
        return {"translation": translation}
    
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# --- Endpoint 5: Word Frequency ---
@app.post("/text/word-frequency")
def word_frequency_endpoint(payload: WordFrequencyRequest):
    # Extract words using regex and count frequencies case-insensitively
    words = re.findall(r'\b\w+\b', payload.text.lower())
    frequency = dict(Counter(words))
    return {"word_frequency": frequency}