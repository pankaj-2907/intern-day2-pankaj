# llm-service 

import os
from google import genai
from dotenv import load_dotenv
from google.genai import types
from fastapi import HTTPException, status
import logging

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API Key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from environment variables.")

client = genai.Client()

# Initialize the model (using gemini-1.5-flash as a fast & reliable choice)
MODEL_NAME = "gemini-flash-latest"

logger = logging.getLogger(__name__)

# Permitted categories as per requirements
PERMITTED_CATEGORIES = {"Technical", "Business", "Education", "General"}

def generate_summary(text: str) -> str:
    """Generates a concise summary of the provided text."""
    prompt = f"Provide a clear and concise summary of the following text:\n\n{text}"
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )
    if not response.text or not response.text.strip():
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="AI provider returned empty generation response."
        )
    return response.text.strip()


def generate_classification(text: str) -> dict:
    """Classifies the text into a category and provides confidence & reasoning."""
    prompt = (
        "Classify the following text into strictly ONE of these categories: Technical, Business, Education, General. "
        "Provide your response in this exact format:\n"
        "Category: [Category Name]\n"
        "Confidence: [Number between 0.0 and 1.0]\n"
        "Reasoning: [Your explanation]\n\n"
        f"Text: {text}"
    )
    
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )
    
    raw_text = response.text.strip() if response.text else ""
    if not raw_text:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="AI provider returned empty generation response."
        )

    # Parsing logic
    category = "General"
    confidence = 0.95
    reasoning = raw_text

    try:
        lines = raw_text.split("\n")
        for line in lines:
            if line.startswith("Category:"):
                category = line.replace("Category:", "").strip()
            elif line.startswith("Confidence:"):
                confidence = float(line.replace("Confidence:", "").strip())
            elif line.startswith("Reasoning:"):
                reasoning = line.replace("Reasoning:", "").strip()
    except Exception as e:
        logger.warning(f"Failed to parse classification output cleanly: {e}")

    # Validate category against permitted values (Task 4 requirement)
    if category not in PERMITTED_CATEGORIES:
        logger.warning(f"Model generated unpermitted category: {category}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="AI model produced invalid output category."
        )

    return {
        "category": category,
        "confidence": confidence,
        "reasoning": reasoning
    }


def generate_sentiment(text: str) -> dict:
    """Analyzes sentiment and returns sentiment, score, and explanation."""
    prompt = (
        "Analyze the sentiment of the following text. "
        "Strictly follow this exact format:\n"
        "Sentiment: [Positive/Neutral/Negative]\n"
        "Score: [Number between -1.0 and 1.0]\n"
        "Explanation: [Brief explanation]\n\n"
        f"Text: {text}"
    )
    
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )
    
    raw_text = response.text.strip() if response.text else ""
    if not raw_text:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="AI provider returned empty generation response."
        )

    sentiment = "Neutral"
    score = 0.0
    explanation = raw_text

    try:
        lines = raw_text.split("\n")
        for line in lines:
            if line.startswith("Sentiment:"):
                sentiment = line.replace("Sentiment:", "").strip()
            elif line.startswith("Score:"):
                score = float(line.replace("Score:", "").strip())
            elif line.startswith("Explanation:"):
                explanation = line.replace("Explanation:", "").strip()
    except Exception as e:
        logger.warning(f"Failed to parse sentiment output cleanly: {e}")

    return {
        "sentiment": sentiment,
        "score": score,
        "explanation": explanation
    }

# def generate_summary(text: str) -> str:
#     """Generates a concise summary of the provided text."""
#     prompt = f"Provide a clear and concise summary of the following text:\n\n{text}"
    
#     response = client.models.generate_content(
#         model=MODEL_NAME,
#         contents=prompt,
#     )

#     return response.text.strip()


# def generate_classification(text: str) -> dict:
#     """Classifies the text into a category and provides reasoning."""
#     prompt = (
       
#         #"Classify the following text into one of these categories: Technical, Business, Education, General. "
#         #"Return the response in a structured format with category, confidence (0.0 to 1.0), and reasoning.\n\n"
        
#         "Classify the following text into one of these categories: Technical, Business, Education, General. "
#         "Return the response in a structured format with category, confidence (0.0 to 1.0), and reasoning.\n\n"
#         f"Text: {text}"
#     )
#     response = client.models.generate_content(
#         model=MODEL_NAME,
#         contents=prompt,
#     )

#     ''' response = client.models.generate_content(
#             model=MODEL_NAME,
#             contents=prompt,
#             config=types.GenerateContentConfig(
#                 temperature=0.7  # Here 0.0 or 1.0 will pass
#             ),
#         ) '''
#     return {
#         "category": "General",
#         "confidence": 0.95,
#         "reasoning": response.text.strip()
#     }


# def generate_sentiment(text: str) -> dict:
#     """Analyzes the sentiment of the provided text."""
#     prompt = (
#         "Analyze the sentiment of the following text (e.g., Positive, Neutral, Negative). "
#         "Provide a sentiment score between -1.0 and 1.0 and a brief explanation.\n\n"
#         f"Text: {text}"
#     )
#     response = client.models.generate_content(
#         model=MODEL_NAME,
#         contents=prompt,
#     )
#     return {
#         "sentiment": "Neutral",
#         "score": 0.0,
#         "explanation": response.text.strip()
#     }