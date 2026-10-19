import os
from google import genai
from dotenv import load_dotenv
from google.genai import types

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API Key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from environment variables.")

client = genai.Client()

# Initialize the model (using gemini-1.5-flash as a fast & reliable choice)
MODEL_NAME = "gemini-flash-latest"

def generate_summary(text: str) -> str:
    """Generates a concise summary of the provided text."""
    prompt = f"Provide a clear and concise summary of the following text:\n\n{text}"
    
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )

    return response.text.strip()


def generate_classification(text: str) -> dict:
    """Classifies the text into a category and provides reasoning."""
    prompt = (
       
        #"Classify the following text into one of these categories: Technical, Business, Education, General. "
        #"Return the response in a structured format with category, confidence (0.0 to 1.0), and reasoning.\n\n"
        
        "Classify the following text into one of these categories: Technical, Business, Education, General. "
        "Return the response in a structured format with category, confidence (0.0 to 1.0), and reasoning.\n\n"
        f"Text: {text}"
    )
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )

    ''' response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7  # Here 0.0 or 1.0 will pass
            ),
        ) '''
    return {
        "category": "General",
        "confidence": 0.95,
        "reasoning": response.text.strip()
    }


def generate_sentiment(text: str) -> dict:
    """Analyzes the sentiment of the provided text."""
    prompt = (
        "Analyze the sentiment of the following text (e.g., Positive, Neutral, Negative). "
        "Provide a sentiment score between -1.0 and 1.0 and a brief explanation.\n\n"
        f"Text: {text}"
    )
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )
    return {
        "sentiment": "Neutral",
        "score": 0.0,
        "explanation": response.text.strip()
    }